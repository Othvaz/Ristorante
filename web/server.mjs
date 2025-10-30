import express, { json } from "express";
import cors from "cors";
import dotenv from "dotenv";
import pkg from "pg";

const { Pool } = pkg;
dotenv.config({ override: true });

const pool = new Pool({ connectionString: process.env.DATABASE_URL });

const app = express();
app.use(cors());
app.use(express.json());
app.use(express.static('public'));
const port = 3000;

const OPENROUTER_BASE = process.env.OPENROUTER_BASE || "https://openrouter.ai/api/v1";
let conversationHistory = [];


app.listen(port, () => {
    console.log(`Server running on port ${port}.`);
});

// COMMANDS FOR SQL AND STUFF
async function getAllRecipes() {
    const theQuery = `
        SELECT recipe_name
        FROM recipes
        ORDER BY recipe_id
        ASC;
    `
    const results = await pool.query(theQuery);
    return results.rows;
}

async function getIngredientFromRecipe(recipeName){
    const theQuery = `
        SELECT
            i.ingredient_name
        FROM
            recipes r
        JOIN
            recipe_ingredients ri ON r.recipe_id = ri.recipe_id
        JOIN
            ingredients i on ri.ingredient_id = i.ingredient_id
        WHERE
            r.recipe_name = '${recipeName}';
    `
    const results = await pool.query(theQuery);
    return results.rows;
}

async function chatter(model, systemText, userText, temperature = 0.2, jsonMode = false, maxTokens = undefined){
    const messages = [];
    if (systemText && systemText.trim() !== "") messages.push({role:"system",content:systemText});
    messages.push({role:"user", content:userText});
    const body = { model, messages, temperature, stream: false };
    if (jsonMode) body.response_format = { type: "json_object" };
    if (maxTokens) body.max_tokens = maxTokens;

    const response = await fetch(`${OPENROUTER_BASE}/chat/completions`, {
        method: "POST",
        headers: {
            "Authorization": `Bearer ${process.env.OPENROUTER_API_KEY}`,
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost",
            "X-Title": "NewsDebateWeb"
        },
        body: JSON.stringify(body)
    });
    if (!response.ok){
        const errorText = await response.text();
        throw new Error(`OpenRouter error ${response.status}: ${errorText}`);
    }
    const data = await response.json();
    return data.choices[0].message.content;
}

async function getRecipesByQuery(recipeName, ingredientName, includeInstructions = true) {
    let query = `
        SELECT DISTINCT r.recipe_id, r.recipe_name, r.instructions
        FROM recipes r
    `;
    const params = [];
    const whereClauses = [];

    if (ingredientName && ingredientName.toUpperCase() !== 'NONE') {
        query += `
            JOIN recipe_ingredients ri ON r.recipe_id = ri.recipe_id
            JOIN ingredients i ON ri.ingredient_id = i.ingredient_id
        `;
        whereClauses.push(`i.ingredient_name ILIKE $${params.length + 1}`);
        params.push(`%${ingredientName}%`);
    }

    if (recipeName && recipeName.toUpperCase() !== 'NONE') {
        whereClauses.push(`r.recipe_name ILIKE $${params.length + 1}`);
        params.push(`%${recipeName}%`);
    }

    if (whereClauses.length > 0) {
        query += ` WHERE ${whereClauses.join(' AND ')}`;
    }
    
    query += ` LIMIT 5;`;

    const { rows } = await pool.query(query, params);
    
    if (rows.length === 0) {
        return "No recipes found matching your criteria.";
    }

    let formattedResults = "";
    for (const recipe of rows) {
        const ingredientsQuery = `
            SELECT i.ingredient_name, ri.quantity, u.unit_name
            FROM recipe_ingredients ri
            JOIN ingredients i ON ri.ingredient_id = i.ingredient_id
            JOIN units u ON ri.unit_id = u.unit_id
            WHERE ri.recipe_id = $1;
        `;
        const ingredientsResult = await pool.query(ingredientsQuery, [recipe.recipe_id]);
        
        const ingredientsList = ingredientsResult.rows.map(ing => 
            `${ing.quantity} ${ing.unit_name} ${ing.ingredient_name}`
        ).join(', ');
        
        formattedResults += `Recipe: ${recipe.recipe_name}\nIngredients: ${ingredientsList}\n`;
        if (includeInstructions) {
            formattedResults += `Instructions: ${recipe.instructions}\n`;
        }
        formattedResults += `---\n`;
    }

    return formattedResults;
}

async function getQuantitiesForRecipe(recipeName) {
    const sql = `
        SELECT i.ingredient_name, ri.quantity, u.unit_name
        FROM recipes r
        JOIN recipe_ingredients ri ON r.recipe_id = ri.recipe_id
        JOIN ingredients i ON ri.ingredient_id = i.ingredient_id
        JOIN units u ON ri.unit_id = u.unit_id
        WHERE r.recipe_name ILIKE $1
        ORDER BY i.ingredient_name;
    `;
    const { rows } = await pool.query(sql, [recipeName]);
    return rows; // [{ ingredient_name, quantity, unit_name }, ...]
}

async function getInstructionForRecipe(recipeName) {
    const sql = `
        SELECT recipe_id, recipe_name, instructions
        FROM recipes
        WHERE recipe_name ILIKE $1
        ORDER BY recipe_id ASC
        LIMIT 1;
    `;
    const { rows } = await pool.query(sql, [recipeName]);
    return rows[0] || null; // { recipe_id, recipe_name, instructions } | null
}

// CONNECTIONS
app.get("/api/getAllRecipes", async(req,res) => {
    try {
        const rows = await getAllRecipes();
        res.json(rows);
    } catch (err) {
        res.status(500).json({error: err.message});
    }
})

app.get("/api/getIngredientFromRecipe", async (req, res) => {
    try {
        const { recipeName } = req.query;
        if (!recipeName) {
            return res.status(400).json({ error: "uhh" });
        }
        const rows = await getIngredientFromRecipe(recipeName);
        res.json(rows);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

app.post("/api/getQuantitiesForRecipe", async (req, res) => {
    try {
        const { recipeName } = req.body || {};
        if (!recipeName) return res.status(400).json({ error: "Missing recipeName." });
        const rows = await getQuantitiesForRecipe(recipeName);
        return res.json(rows);
    } catch (err) {
        console.error("Error in getQuantitiesForRecipe:", err);
        res.status(500).json({ error: err.message });
    }
});

app.post("/api/getInstructionsForRecipe", async (req, res) => {
    try {
        const { recipeName } = req.body || {};
        if (!recipeName) return res.status(400).json({ error: "Missing recipeName." });
        const row = await getInstructionForRecipe(recipeName);
        if (!row) return res.status(404).json({ error: "Recipe not found." });
        return res.json(row); // { recipe_id, recipe_name, instructions }
    } catch (err) {
        console.error("Error in getInstructionsForRecipe:", err);
        res.status(500).json({ error: err.message });
    }
});

app.post("/api/chat", async (req, res) => {
    try {
        const { message } = req.body;

        if (!message) {
            return res.status(400).json({ error: "Message cannot be empty." });
        }
        conversationHistory.push({ role: 'user', content: message });
        if (conversationHistory.length > 6) {
            conversationHistory = conversationHistory.slice(-6);
        }

        const systemPrompt = `You are a specialized AI assistant for a recipe website. Your function is to parse user requests and return ONLY a valid JSON object.
        The JSON object must have three keys: "recipeName", "ingredientName", and "includeInstructions".

        - "recipeName": Extract the recipe name. If not specified, use the string "NONE".
        - "ingredientName": Extract the primary ingredient. If not specified, use the string "NONE".
        - "includeInstructions": This must be a boolean. It should be 'false' ONLY if the user explicitly asks to exclude instructions (e.g., "no instructions", "don't show the steps"). Otherwise, the default value MUST be 'true'.

        Examples:
        - User: "Show me how to make Beef Stroganoff" -> {"recipeName": "Beef Stroganoff", "ingredientName": "NONE", "includeInstructions": true}
        - User: "Any recipes with chicken?" -> {"recipeName": "NONE", "ingredientName": "chicken", "includeInstructions": true}
        - User: "Give me the ingredients for Carbonara. No instructions please." -> {"recipeName": "Carbonara", "ingredientName": "NONE", "includeInstructions": false}
        - User: "hey how are you doing" -> {"recipeName": "NONE", "ingredientName": "NONE", "includeInstructions": true}
        
        Do not add any other text, explanations, or conversational filler. Strictly output only the JSON object.`;

        const model = "google/gemini-2.5-flash-preview-09-2025";

        const chatbotReply = await chatter(model, systemPrompt, message, 0.2, true);
        
        const parsedData = JSON.parse(chatbotReply);

        res.json({ searchParams: parsedData });

    } catch (err) {
        console.error("Error in chat endpoint:", err);
        res.status(500).json({ error: err.message });
    }
});

app.post("/api/get-recipe-details", async (req, res) => {
    try {
        const { searchParams } = req.body;
        if (!searchParams) {
            return res.status(400).json({ error: "Missing search parameters." });
        }
        const { recipeName, ingredientName, includeInstructions } = searchParams;
        const dbResults = await getRecipesByQuery(recipeName, ingredientName, includeInstructions);

        const extractFirstRecipeName = (resultsStr) => {
            if (!resultsStr || typeof resultsStr !== "string") return null;
            if (/No recipes found/i.test(resultsStr)) return null;
            const m = resultsStr.match(/^\s*Recipe:\s*(.+)$/m);
            return m ? m[1].trim() : null;
        };
        
        const recipeNameReal = extractFirstRecipeName(dbResults) || (recipeName && recipeName.toUpperCase() !== 'NONE' ? recipeName : null) || 'Recipe';
        
        const historyText = conversationHistory.map(turn => `${turn.role}: ${turn.content}`).join('\n');
        const finalSystemPrompt = `You are a helpful and friendly recipe assistant. Your goal is to answer the user's question in a natural, conversational way based on the provided database results and the conversation history.

        <CONVERSATION_HISTORY>
        ${historyText}
        </CONVERSATION_HISTORY>

        <DATABASE_RESULTS>  
        ${dbResults}
        </DATABASE_RESULTS>

        Based on the information above, provide a comprehensive and helpful response to the user's latest message. If the database found results, present them clearly. If no results were found, inform the user politely. If the user asked for no instructions, confirm that you have omitted them.`;

        const model = "google/gemini-2.5-flash-preview-09-2025"; 
        const lastUserMessage = conversationHistory.findLast(m => m.role === 'user')?.content || "";
        const naturalReply = await chatter(model, finalSystemPrompt, lastUserMessage, 0.5);

        const formattedReply = `//${recipeNameReal}//\n\n${naturalReply}`;
        
        conversationHistory.push({ role: 'assistant', content: naturalReply });

        res.json({ reply: formattedReply });

    } catch (err) {
        console.error("Error in get-recipe-details endpoint:", err);
        res.status(500).json({ error: err.message });
    }
});