```javascript
/**
 * Node.js webhook function for Dialogflow CX using Gemini API.
 *
 * This function handles candidate questions outside the standard recruitment flow by:
 * 1. Receiving the user's question from Dialogflow CX.
 * 2. Using Google's Generative AI (Gemini) to generate a relevant answer based on the job description.
 * 3. Returning the answer to Dialogflow CX in the correct format.
 * 4. Maintaining conversation context to continue the standard flow afterward.
 */

const { VertexAI } = require('@google-cloud/vertexai');

// Replace with your Google Cloud project ID and the Gemini model name.
const PROJECT_ID = 'YOUR_PROJECT_ID'; //  e.g., 'my-gcp-project'
const LOCATION = 'us-central1'; // Or any location that supports Gemini API
const MODEL_NAME = 'gemini-1.0-pro'; // Or any Gemini model you want to use


/**
 * Job Details - This should ideally come from a database or configuration,
 * not hardcoded in a real-world application. For this example, it's defined inline.
 */
const jobDetails = {
    "position_title": "CDL Truck Driver",
    "company_name": "FedX",
    "required_experience": "Minimum 1 year of verifiable OTR experience",
    "required_skills": [
        "Safely operate a Class A tractor-trailer",
        "Complete pre-trip and post-trip inspections",
        "Load and unload freight",
        "Maintain accurate logs using ELD system",
        "Communicate effectively with dispatch and customers",
        "Follow all DOT regulations and company safety policies"
    ],
    "required_qualifications": [
        "Valid Class A Commercial Driver's License",
        "Clean MVR with no more than 2 moving violations in the past 3 years",
        "No DUIs or reckless driving convictions",
        "Must be at least 23 years of age",
        "Must pass DOT physical and drug screen",
        "High school diploma or GED preferred"
    ],
    "pay_rate": "$0.58-$0.65 per mile based on experience, Average weekly miles: 2,500-3,000, Weekly pay with direct deposit, Sign-on bonus: $3,000 (paid in installments), Safety bonuses up to $500 quarterly",
    "schedule_type": "Regional routes with 2-3 nights home per week",
    "location": "Midwest, routes within 500-mile radius of Chicago terminal",
    "benefits": [
        "Medical, dental, and vision insurance after 60 days",
        "401(k) with 3% company match after 90 days",
        "Paid vacation (1 week after first year)",
        "Paid holidays",
        "Referral bonuses: $1,500 per hired driver"
    ],
    "job_description": "Transporting various goods to customers within a 500-mile radius of the Chicago terminal. Routes allow you to be home 2-3 nights per week.",
    "screening_requirements": [
        "DOT physical",
        "Drug screen",
        "MVR check (clean record)",
        "Background check implied by MVR/DUI requirements"
    ],
    "common_candidate_questions": [
        "What type of freight will I be hauling?",
        "What is the truck's make and model, and is it an automatic or manual transmission?",
        "What are the typical start and end times for a run?",
        "What is the breakdown policy and procedure?",
        "How is the sign-on bonus paid out?",
        "What are the specific routes I'll be running?",
        "Can you provide more details about the safety bonus program?",
        "What are the advancement opportunities within the company?"
    ],
    "question_answers": {
        "What type of freight will I be hauling?": "You'll be hauling general freight, primarily [specify type if known, e.g., consumer goods, electronics].",
        "What is the truck's make and model, and is it an automatic or manual transmission?": "We primarily use [Truck Make and Model, e.g., Freightliner Cascadias]. Most trucks are [Automatic/Manual] transmission.",
        "What are the typical start and end times for a run?": "Start times vary depending on the route, but typically between [Time] and [Time]. End times are dependent on mileage and delivery schedules.",
        "What is the breakdown policy and procedure?": "We have a 24/7 maintenance team available. In case of a breakdown, contact dispatch immediately. They will guide you through the next steps and ensure roadside assistance if needed.",
        "How is the sign-on bonus paid out?": "The $3,000 sign-on bonus is paid out in installments. Typically, it's spread over [Number] months, with the first payment after [Timeframe].",
        "What are the specific routes I'll be running?": "You will be running regional routes within a 500-mile radius of the Chicago terminal, covering areas in the Midwest.",
        "Can you provide more details about the safety bonus program?": "The safety bonus program awards up to $500 quarterly for drivers with a clean safety record, no preventable accidents, and adherence to all company policies.",
        "What are the advancement opportunities within the company?": "We encourage career growth within FedX. Opportunities include lead driver positions, driver training, and potentially management roles depending on performance and interest."
    },
    "objection_handling": {
        "Pay is lower than another offer": "We understand pay is important. While our starting mileage rate may be slightly lower, we offer consistent miles (2,500-3,000 weekly), frequent home time (2-3 nights a week), and valuable benefits like health insurance and a 401(k) match. When you factor in everything, the overall compensation package is very competitive. Can you share details about the other offer so we can compare apples to apples?",
        "Home time isn't guaranteed": "While unexpected delays can occasionally happen in trucking, we prioritize getting our drivers home as scheduled. Our regional routes are specifically designed to get you home 2-3 nights per week. We work hard to minimize disruptions and communicate proactively about any potential issues.",
        "Concerns about the ELD system": "Our ELD system is user-friendly and designed to streamline your workflow. We provide comprehensive training on the system, and our dispatch team is always available to answer your questions and provide support."
    },
    "key_screening_questions": [
        "Do you possess a valid Class A Commercial Driver's License?",
        "Can you provide a copy of your MVR for review?",
        "Do you have at least 1 year of verifiable OTR experience?",
        "Have you ever had a DUI or reckless driving conviction?",
        "Are you currently taking any medications that may affect your ability to drive safely?",
        "Are you comfortable using an ELD system for logging hours of service?",
        "Are you able to pass a DOT physical and drug screen?",
        "Are you familiar with DOT regulations and company safety policies?"
    ],
    "age_requirement": "23",
    "qualification_checks": [
        "Valid Class A CDL",
        "DOT Medical Card (Verification)",
        "MVR (Motor Vehicle Record)",
        "PSP (Pre-Employment Screening Program) Report",
        "Verifiable OTR Experience (Check previous employers)",
        "Background Check (If not covered sufficiently by MVR/PSP)"
    ]
};



/**
 * Initializes the Vertex AI client. This should be done outside the main function
 * to reuse the client across multiple invocations of the Cloud Function.
 */
const vertexAI = new VertexAI({ project: PROJECT_ID, location: LOCATION });

/**
 * Gets the Gemini Pro model
 */
const model = vertexAI.getGenerativeModel({
    model: MODEL_NAME,
    generation_config: {
        maxOutputTokens: 2048,
        temperature: 0.9,
        topP: 1,
    },
    safety_settings: [{
        category: 'HARM_CATEGORY_HARASSMENT',
        threshold: 'BLOCK_MEDIUM_AND_ABOVE'
    }, {
        category: 'HARM_CATEGORY_HATE_SPEECH',
        threshold: 'BLOCK_MEDIUM_AND_ABOVE'
    }, {
        category: 'HARM_CATEGORY_SEXUALLY_EXPLICIT',
        threshold: 'BLOCK_MEDIUM_AND_ABOVE'
    }, {
        category: 'HARM_CATEGORY_DANGEROUS_CONTENT',
        threshold: 'BLOCK_MEDIUM_AND_ABOVE'
    }],
});


/**
 * Cloud Function to handle Dialogflow CX webhook requests.
 *
 * @param {Object} req Cloud Function request object.
 * @param {Object} res Cloud Function response object.
 */
exports.dialogflowCXWebhook = async (req, res) => {
    try {
        console.log("Request body:", JSON.stringify(req.body, null, 2)); // Log the request body for debugging

        // Extract user's question from Dialogflow CX request.  Use a fallback if not found.
        const queryText = req.body.fulfillmentInfo?.parameters?.query || req.body.queryResult?.queryText || "Tell me about the job"; // Access queryText safely

        if (!queryText) {
            console.error("Error: Could not extract query text from request.");
            return res.status(400).send({
                fulfillmentText: "Sorry, I didn't understand the question. Please try again.",
            });
        }

        // Construct the prompt for Gemini.  This combines the job details with the user's question.
        const prompt = `You are a helpful AI assistant providing information about a CDL Truck Driver position at FedX.  Answer the following question based on the provided job details.  If the information is not explicitly in the job details, respond with 'I am sorry, that is not described in this job posting.'\n\nJob Details:\n${JSON.stringify(jobDetails, null, 2)}\n\nQuestion: ${queryText}`;


        // Call the Gemini API to generate an answer.
        let geminiResponse;
        try {
             const streamingResp = await model.generateContentStream({
                contents: [{ role: 'user', parts: [{ text: prompt }] }],
            });

            let geminiTextResponse = "";
              for await (const chunk of streamingResp.stream) {
                  geminiTextResponse += chunk.text;
              }
            geminiResponse = geminiTextResponse;


            if (!geminiResponse || geminiResponse.length === 0) {
                console.error("Error: Gemini API returned an empty response.");
                return res.status(500).send({
                    fulfillmentText: "Sorry, I couldn't generate an answer at this time. Please try again later.",
                });
            }
        } catch (error) {
            console.error("Error calling Gemini API:", error);
            return res.status(500).send({
                fulfillmentText: "Sorry, I encountered an error generating the response. Please try again later.",
            });
        }



        // Format the response for Dialogflow CX.
        const fulfillmentResponse = {
            fulfillmentText: geminiResponse,
            // You can add other fields like payload, sessionInfo, etc., as needed.
        };

        console.log("Fulfillment Response:", JSON.stringify(fulfillmentResponse, null, 2)); // Log the response for debugging.

        // Send the response back to Dialogflow CX.
        res.status(200).send(fulfillmentResponse);

    } catch (error) {
        console.error("General error in webhook:", error);
        res.status(500).send({
            fulfillmentText: "Sorry, there was an unexpected error.  Please try again later.",
        });
    }
};


/**
 * Helper function to extract parameters from the Dialogflow CX request.
 *  Deprecated as no longer used directly. Keeping here for potential future use.
 * @param {Object} requestBody The request body from Dialogflow CX.
 * @param {string} parameterName The name of the parameter to extract.
 * @returns {string | null} The value of the parameter, or null if not found.
 */
function getParameter(requestBody, parameterName) {
    try {
        return requestBody.fulfillmentInfo.parameters[parameterName];
    } catch (error) {
        console.warn(`Parameter '${parameterName}' not found in request or malformed request.`);
        return null;
    }
}

```

**Explanation:**

1.  **Dependencies:** The code uses the `@google-cloud/vertexai` library for interacting with the Gemini API. Make sure to install it using `npm install @google-cloud/vertexai`.

2.  **Configuration:**
    *   `PROJECT_ID`: Replace this with your Google Cloud project ID.
    *   `LOCATION`:  Set the correct region for Gemini.  `us-central1` is a common choice, but check the documentation.
    *   `MODEL_NAME`:  Specifies the Gemini model you're using (e.g., `gemini-1.0-pro`).  Refer to the Gemini API documentation for available models.

3.  **`jobDetails`:** This object holds the job description and details.  In a real application, this data would come from a database or external configuration instead of being hardcoded.

4.  **`vertexAI` and `model` Initialization:** The `VertexAI` client and the Gemini model are initialized *outside* the `dialogflowCXWebhook` function.  This is crucial for performance.  Initializing them inside the function would create a new client on every request, which is inefficient.

5.  **`dialogflowCXWebhook` Function:** This is the core of the webhook.
    *   **Request Handling:** It receives the `req` (request) and `res` (response) objects from Cloud Functions.
    *   **Error Handling:** It includes a `try...catch` block to handle potential errors during the process.
    *   **Logging:**  `console.log` statements are used to log the request body and the fulfillment response for debugging purposes.  These are very useful when troubleshooting.
    *   **Extracting the Query:** It extracts the user's question (`queryText`) from the Dialogflow CX request. It uses a fallback mechanism to handle different request formats, and includes an error check to gracefully handle cases where the query is missing.
    *   **Prompt Construction:** This is a crucial step. It builds a prompt that combines the job details and the user's question.  The prompt instructs Gemini on how to act (as a helpful assistant) and what context to use.  The prompt is carefully crafted to guide the AI model's response.  Crucially, it specifies how to respond if information is not present in the job details.
    *   **Calling the Gemini API:**  The code calls the Gemini API to generate an answer based on the prompt.  It uses the `generateContent` method of the model.  Error handling is included to catch potential API errors. Streaming is used to generate content, and then collected into a single string.
    *   **Response Formatting:**  The generated answer is formatted into a `fulfillmentResponse` object that Dialogflow CX can understand.  This includes the `fulfillmentText` which contains the answer to be displayed to the user.
    *   **Sending the Response:** The `fulfillmentResponse` is sent back to Dialogflow CX.
    *   **Deprecation of Parameter Extraction:**  The `getParameter` function is included for possible future use.  The main function accesses the `queryText` in a more direct way.

**Deployment to Cloud Functions:**

1.  **Create a Google Cloud Project:** If you don't have one, create a Google Cloud project.
2.  **Enable the Cloud Functions API and Vertex AI API:** In the Google Cloud Console, enable the Cloud Functions API and the Vertex AI API for your project.
3.  **Create a Service Account:** Create a service account with the `Cloud Functions Invoker` and `Vertex AI User` roles.  Download the JSON key file for the service account.  This is what allows the cloud function to securely call Gemini.
4.  **Install the Google Cloud SDK:**  Install and configure the Google Cloud SDK (`gcloud`).
5.  **Create a `package.json` File:**  Create a `package.json` file in the same directory as your `index.js` file (where you've saved the code).  The `package.json` file should look something like this:

    ```json
    {
      "name": "dialogflow-cx-webhook",
      "version": "1.0.0",
      "description": "Dialogflow CX Webhook for Gemini",
      "main": "index.js",
      "scripts": {
        "start": "node index.js"
      },
      "dependencies": {
        "@google-cloud/vertexai": "^3.3.0"
      },
      "engines": {
        "node": ">=18"  // or higher compatible with Vertex AI
      }
    }
    ```

    Make sure to use Node version 18 or higher, as this is more compatible with `@google-cloud/vertexai` and Vertex AI in general. Run `npm install` to install the dependencies.
6.  **Deploy the Cloud Function:**  Use the `gcloud` command to deploy the function:

    ```bash
    gcloud functions deploy dialogflowCXWebhook \
    --runtime nodejs18 \
    --trigger-http \
    --allow-unauthenticated \
    --entry-point dialogflowCXWebhook \
    --service-account=<YOUR_SERVICE_ACCOUNT_EMAIL>
    ```

    *   Replace `dialogflowCXWebhook` with the name of your function.
    *   Replace `nodejs18` with the appropriate Node.js runtime.
    *   Replace `<YOUR_SERVICE_ACCOUNT_EMAIL>` with the email address of the service account you created.  This is crucial to grant the function permissions.
    *   `--allow-unauthenticated` makes the function publicly accessible.  For production environments, you should restrict access appropriately.  Consider using Identity-Aware Proxy (IAP).

7.  **Get the Cloud Function URL:** After deployment, the `gcloud` command will output the URL of your Cloud Function.  You'll need this URL to configure the webhook in Dialogflow CX.

**Configuring the Webhook in Dialogflow CX:**

1.  **Open Dialogflow CX Console:** Go to the Dialogflow CX console.
2.  **Select Your Agent:** Choose the agent you want to configure.
3.  **Go to Agent Settings:** Click on the "Agent Settings" icon (gear icon) in the left sidebar.
4.  **Select the "Advanced" Tab:**
5.  **Enable Webhooks:** Toggle the "Enable webhook calls" switch to "on".
6.  **Add a New Webhook:** Click the "Add webhook" button.
7.  **Configure the Webhook:**
    *   **Webhook Name:** Give your webhook a descriptive name (e.g., "GeminiFallbackWebhook").
    *   **Service Endpoint:** Enter the URL of your deployed Cloud Function.
    *   **Authentication:**  If your Cloud Function requires authentication (it shouldn't if you used `--allow-unauthenticated`), configure the appropriate authentication method (e.g., using a service account token).  For a basic setup, leave this empty if you used `--allow-unauthenticated`.
    *   **Request/Response:**  Leave the default settings.  Dialogflow CX expects a specific JSON format for requests and responses.
8.  **Save the Webhook:** Click the "Save" button.
9.  **Configure Route:**
    *   In Dialogflow CX, navigate to the flow where you want to use the webhook.
    *   Create a new route, or modify an existing one.
    *   In the route's "Condition" field, you can use a conditional expression to trigger the webhook when the user's question is outside the standard recruitment flow. For example, you could use the `$intent.name != "your_recruitment_intent"` condition.  You'll need to have a separate intent that handles the standard recruitment flow.  This is a key part of the setup - you need to differentiate when to use the standard intents vs. when to fire the webhook.
    *   In the route's "Transition" section, choose "Webhook" and select the webhook you just created.
10. **Test:** Test your Dialogflow CX agent with questions that fall outside the standard recruitment flow to ensure the webhook is triggered and the Gemini API provides relevant answers.

**Important Considerations:**

*   **Cost:**  Using the Gemini API incurs costs. Be aware of the pricing and monitor your usage.
*   **Security:**  If you are handling sensitive data, implement appropriate security measures to protect the data in transit and at rest.
*   **Prompt Engineering:**  The quality of the Gemini-generated answers depends heavily on the prompt you provide. Experiment with different prompt designs to optimize the results.  Clear, concise instructions are key.
*   **Job Details Source:** In a production environment, retrieve the `jobDetails` from a database or configuration service.  Avoid hardcoding it in the function. This makes the function more maintainable and allows you to easily update the job details without redeploying the function.
*   **Context Management:**  The example maintains context by simply returning a `fulfillmentText`. You might want to use Dialogflow CX's session parameters to maintain more complex conversation state.  Store relevant information in session parameters and retrieve it in subsequent webhook calls.
*   **Latency:** Calling the Gemini API adds latency to the response.  Consider implementing mechanisms to improve the user experience, such as displaying a "Thinking..." message while waiting for the API to respond.
*   **Error Handling:** The provided code includes basic error handling, but you should enhance it to handle specific error cases and provide more informative error messages to the user.
*   **Rate Limiting:**  The Gemini API may have rate limits. Implement error handling to gracefully handle rate limit errors and potentially retry requests.
*   **Safety:** Vertex AI's safety settings are included, but carefully review and adjust them to suit your specific requirements and risk tolerance.
*   **Testing:** Thoroughly test your webhook with a variety of questions and scenarios to ensure it behaves as expected.
*   **Continuous Improvement:** Monitor the performance of your webhook and the quality of the Gemini-generated answers.  Continuously refine your prompts and job details to improve the user experience.

This comprehensive solution provides a robust framework for integrating Gemini with Dialogflow CX to handle candidate questions outside the standard recruitment flow. Remember to adapt the code and configuration to your specific needs and environment.
