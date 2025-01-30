// Function to evaluate basic expressions
function evaluateExpression(expr) {
    try {
        expr = expr.trim();
        // Check for basic arithmetic validity (numbers, operators, parentheses)
        if (/^[\d+\-*/().\s]+$/.test(expr)) {
            return eval(expr);  // Use JavaScript eval for arithmetic
        } else {
            return "Error: Invalid arithmetic expression - " + expr;
        }
    } catch (e) {
        return "Error: " + e.message;
    }
}

// Simulate 'ullitu' user input
function ullitu(prompt) {
    const userInput = document.getElementById('user-input').value;
    return userInput ? `${prompt}: ${userInput}` : 'No input provided';
}

// Main function to handle running the code
function runCode() {
    const code = document.getElementById('code-input').value;
    const outputElement = document.getElementById('output');
    let output = '';

    const statements = code.split('\n');
    
    statements.forEach(statement => {
        statement = statement.trim();

        if (statement.startsWith("accu(")) {
            // Handle 'accu' function (similar to print)
            const content = statement.match(/accu\((.*?)\)/);
            if (content) {
                let parts = content[1].split(',').map(p => p.trim());
                let result = '';
                parts.forEach(part => {
                    if (/^".*"$/.test(part)) {
                        result += part.slice(1, -1);  // Remove quotes
                    } else if (/^[\d+\-*/().\s]+$/.test(part)) {
                        result += evaluateExpression(part);
                    } else if (part.includes("ullitu")) {
                        const prompt = part.match(/ullitu\("(.*?)"\)/);
                        if (prompt) {
                            result += ullitu(prompt[1]);
                        }
                    }
                });
                output += result + '\n';
            }
        } else {
            output += "Error: Invalid content - " + statement + '\n';
        }
    });

    outputElement.textContent = output;
}
