```javascript
/**
 * Node.js webhook function for Dialogflow CX using Gemini (Generative AI).
 *
 * This function processes candidate questions, uses Gemini to generate answers based on
 * the provided job description, and returns the answer to Dialogflow CX. It also
 * maintains conversation context for seamless integration with standard flows.
 */

const { VertexAI } = require('@google-cloud/vertexai'); // Updated Import
// Import Dialogflow CX Types
const { SessionsClient } = require('@google-cloud/dialogflow-cx');

// Replace with your Google Cloud project ID
const PROJECT_ID = 'YOUR_PROJECT_ID';

// Replace with the location of your Dialogflow CX agent and Cloud Function
const LOCATION = 'global'; // Or 'us-central1' etc.
const VERTEX_AI_LOCATION = 'us-central1'; // Location for Vertex AI.  It is very important that you choose the location where your gemini API access is permitted.

// Replace with your Gemini model name
const MODEL_NAME = 'gemini-1.5-pro'; // Or 'gemini-pro' etc. Check Vertex AI documentation for available models.

// Define Job Details (context)
const jobDetails = {
  "position_title": "cdl truck driver",
  "company_name": "fedx",
  "required_experience": "Minimum 1 year of verifiable OTR experience",
  "required_skills": [
    "Operating Class A tractor-trailer",
    "Pre-trip and post-trip inspections",
    "Loading and unloading freight (touch freight)",
    "ELD system usage",
    "Communication with dispatch and customers",
    "DOT regulations and company safety policies adherence",
    "Freight delivery on time and damage-free"
  ],
  "required_qualifications": [
    "Valid Class A Commercial Driver's License",
    "Clean MVR (no more than 2 moving violations in past 3 years)",
    "No DUIs or reckless driving convictions",
    "Minimum age of 23",
    "DOT physical",
    "High school diploma or GED (preferred)"
  ],
  "pay_rate": "$0.58-$0.65 per mile based on experience; Average weekly miles: 2,500-3,000; Weekly pay with direct deposit",
  "schedule_type": "Regional routes",
  "location": "Midwest, within 500-mile radius of Chicago terminal",
  "benefits": [
    "Sign-on bonus: $3,000 (paid in installments)",
    "Safety bonuses up to $500 quarterly",
    "Medical, dental, and vision insurance after 60 days",
    "401(k) with 3% company match after 90 days",
    "Paid vacation (1 week after first year)",
    "Paid holidays",
    "Referral bonuses: $1,500 per hired driver",
    "Newer equipment with latest safety features"
  ],
  "job_description": "Transporting various goods to customers within a 500-mile radius of the Chicago terminal. Drivers are typically home 2-3 nights per week.",
  "screening_requirements": [
    "DOT physical",
    "Drug screen"
  ],
  "common_candidate_questions": [
    "What is the average age and mileage of the trucks?",
    "What type of freight will I be hauling?",
    "What is the dispatch process like?",
    "How is detention time handled and compensated?",
    "What are the opportunities for career advancement?",
    "What are the specific routes I would be running?",
    "What is the company culture like? Is there good communication and support for drivers?",
    "How does the sign-on bonus get paid out?"
  ],
  "question_answers": {
    "What is the average age and mileage of the trucks?": "The fleet is newer with trucks typically being no more than 3 years old. They are well maintained, and equipped with safety features. Mileage varies, but preventative maintenance schedules are strict.",
    "What type of freight will I be hauling?": "You'll be hauling general commodities, primarily [mention specific commodities, e.g., consumer goods, auto parts]. Touch freight may be involved.",
    "What is the dispatch process like?": "We use a driver-friendly dispatch system. You will communicate with a dedicated dispatcher who is available to assist you. We aim for efficient route planning and minimal downtime.",
    "How is detention time handled and compensated?": "Detention time is compensated after [mention time, e.g., 2 hours] at a rate of [mention rate, e.g., $20/hour] when properly documented.",
    "What are the opportunities for career advancement?": "We offer opportunities for experienced drivers to become driver trainers, lead drivers, or move into dispatch or management roles.",
    "What are the specific routes I would be running?": "You'll be running regional routes within a 500-mile radius of the Chicago terminal, primarily in the Midwest.  You can expect to be home 2-3 nights per week.",
    "What is the company culture like? Is there good communication and support for drivers?": "We pride ourselves on a supportive and communicative culture.  We have regular driver meetings, open-door policies, and dedicated driver support teams.",
    "How does the sign-on bonus get paid out?": "The sign-on bonus is paid out in installments, typically over the first [Number] months of employment. Specific payment schedules will be detailed in your offer letter."
  },
  "objection_handling": {
    "Low mileage compared to other companies": "While our average weekly mileage is 2,500-3,000, we prioritize driver safety and home time. We offer consistent miles and pay that reflects a sustainable work-life balance. We also offer bonus potential for exceeding targets.",
    "Touch freight": "While some loads may require touch freight, we strive to minimize this. You will be compensated appropriately for any loading or unloading involved.",
    "Concerns about company stability": "FedEx is a well-established company with a long history of success. We are committed to investing in our drivers and providing a stable and secure work environment.",
    "Benefits don't start immediately": "While benefits begin after 60/90 days, it allows us to ensure employees are fully integrated into the company before becoming eligible. We believe that by that time, employees are happy with their new employment choice and are a valuable asset to the team. We also offer competitive pay and bonuses to compensate for the initial waiting period."
  },
  "key_screening_questions": [
    "Can you describe your experience operating a Class A tractor-trailer?",
    "Tell me about your experience with ELD systems.",
    "Have you had any moving violations or accidents in the past 3 years? Please explain.",
    "Are you familiar with DOT regulations and safety policies?",
    "Are you comfortable with regional routes and being home 2-3 nights per week?",
    "Can you provide verifiable employment history for the past 3 years?",
    "Do you have any experience with touch freight or unloading procedures?",
    "What are your salary expectations?"
  ],
  "age_requirement": "23",
  "qualification_checks": [
    "Valid Class A Commercial Driver's License (CDL)",
    "DOT Medical Card",
    "Clean MVR (Motor Vehicle Record)",
    "Verifiable OTR Experience",
    "Drug Screen Results (Negative)",
    "Background Check Clearance"
  ]
};

/**
 * Generates an answer using Google's Gemini model.
 *
 * @param {string} question The candidate's question.
 * @param {object} jobDetails The job details as context.
 * @returns {Promise<string>} The generated answer.
 */
async function generateAnswerWithGemini(question, jobDetails) {
  try {
    // Initialize Vertex AI
    const vertexAI = new VertexAI({ project: PROJECT_ID, location: VERTEX_AI_LOCATION }); // Correctly initialized
    const model = vertexAI.getGenerativeModel({
      model: MODEL_NAME,
      generation_config: {
        maxOutputTokens: 2048,  //Adjust this for longer answers
        temperature: 0.5,
        topP: 1,
        topK: 32,
      },
      safety_settings: [
        {
          category: 'HARM_CATEGORY_HARASSMENT',
          threshold: 'BLOCK_MEDIUM_AND_ABOVE',
        },
        {
          category: 'HARM_CATEGORY_HATE_SPEECH',
          threshold: 'BLOCK_MEDIUM_AND_ABOVE',
        },
        {
          category: 'HARM_CATEGORY_SEXUALLY_EXPLICIT',
          threshold: 'BLOCK_MEDIUM_AND_ABOVE',
        },
        {
          category: 'HARM_CATEGORY_DANGEROUS_CONTENT',
          threshold: 'BLOCK_MEDIUM_AND_ABOVE',
        },
      ],
    });

    // Construct the prompt for Gemini. Make it very clear what you want.
    const prompt = `You are a helpful and informative AI assistant specialized in answering questions about truck driving jobs.  Your goal is to provide concise and helpful answers to candidates, based on the following job details:

    ${JSON.stringify(jobDetails, null, 2)}

    Answer the following question: ${question}

    Be clear, concise, and avoid being overly verbose.  If the question is irrelevant or you can't answer it based on the context, say "I'm sorry, I don't have enough information to answer that."`;

    const streamingResp = await model.generateContentStream(prompt);
    const aggregatedResponse = await streamingResp.response;
    const geminiAnswer = aggregatedResponse.candidates[0].content.parts[0].text;

    return geminiAnswer;

  } catch (error) {
    console.error('Gemini API Error:', error);
    throw new Error(`Failed to generate answer with Gemini: ${error.message}`); // More informative error
  }
}


/**
 * Cloud Functions HTTP function.
 *
 * @param {object} req Cloud Functions request object.
 * @param {object} res Cloud Functions response object.
 */
exports.dialogflowCXWebhook = async (req, res) => {
  console.log('Dialogflow CX Webhook Request Body:', JSON.stringify(req.body));  // Log request for debugging

  try {
    // 1. Extract Data from Dialogflow CX Request
    const queryText = req.body.fulfillmentInfo.tag; // Use the fulfillment tag as a trigger.  Example:  "ask_gemini"
    const sessionInfo = req.body.sessionInfo;
    const sessionPath = sessionInfo.session;
    const parameters = req.body.sessionInfo.parameters;

    // Ensure 'queryText' from the Dialogflow CX tag is the correct trigger
    if (queryText === 'ask_gemini') {
      const candidateQuestion = parameters.candidate_question;  // Access parameter from CX

      if (!candidateQuestion) {
        console.error('No candidate question provided.');
        return res.status(400).send({
          fulfillmentResponse: {
            messages: [{
              text: {
                text: ['I am sorry, I did not receive the question. Please try again.']
              }
            }]
          }
        });
      }

      // 2. Generate Answer Using Gemini
      let geminiResponse;
      try {
        geminiResponse = await generateAnswerWithGemini(candidateQuestion, jobDetails);
      } catch (geminiError) {
        console.error('Error generating response from Gemini:', geminiError);
        return res.status(500).send({
          fulfillmentResponse: {
            messages: [{
              text: {
                text: ['I am having trouble connecting to the AI service. Please try again later.']
              }
            }]
          }
        });
      }

      // 3.  Send Response back to Dialogflow CX
      const responseData = {
        fulfillmentResponse: {
          messages: [
            {
              text: {
                text: [geminiResponse] // The generated answer
              }
            }
          ],
          // Optionally, you can set new parameters or modify existing ones to maintain context.
          //Example:  parameterChanges: [{name: 'some_parameter', value: 'some_value'}]
        }
      };

      console.log('Dialogflow CX Webhook Response:', JSON.stringify(responseData)); // Log the response

      res.status(200).send(responseData);

    } else {
      // If the fulfillment tag is not 'ask_gemini', return a default response
      console.log('No Gemini trigger');
      res.status(200).send({}); // Send an empty response to let CX continue the flow
    }

  } catch (error) {
    console.error('Webhook Error:', error);
    res.status(500).send({ error: `Webhook failed: ${error.message}` }); // Send error response to Dialogflow CX
  }
};


/**
 * Optional: Example function to reset the context (parameters) in a Dialogflow CX Session.
 * Useful for testing or when you want to clear the session.
 *
 * @param {string} projectId The Google Cloud project ID.
 * @param {string} location The location of the Dialogflow CX agent.
 * @param {string} sessionId The ID of the Dialogflow CX session.
 */
async function resetDialogflowCXContext(projectId, location, sessionId) {
  // [START dialogflow_cx_v3_beta1_session_client]
  /**
   * Demonstrates basic session interacting with Dialogflow CX.
   * @param {string} projectId The project to be used
   *   eg. 'PROJECT_ID'
   * @param {string} location The agent location to be used
   *   eg. 'us-central1'
   * @param {string} sessionId A unique identifier for the session
   *   eg. 'SESSION_ID'
   */
  // Imports the Google Cloud client library

  // Instantiates a client
  const client = new SessionsClient({ apiEndpoint: 'global-dialogflow.googleapis.com' });

  async function resetContext() {
    // Construct request
    const sessionPath = client.sessionPath(projectId, location, sessionId);
    const request = {
      session: sessionPath,
      queryInput: {
        input: {
          text: {
            text: "reset",
          },
        },
        config: {
          languageCode: "en",
        },
      },
    };

    // Make request
    const [response] = await client.detectIntent(request);
    console.log(response);
    // [END dialogflow_cx_v3_beta1_session_client]
  }
  await resetContext();
}

// [END all]

```

**Explanation:**

1.  **Dependencies:** Includes necessary libraries: `@google-cloud/vertexai` (for Gemini), and `@google-cloud/dialogflow-cx` (for Dialogflow CX interaction).  Make sure to install these with `npm install @google-cloud/vertexai @google-cloud/dialogflow-cx`.
2.  **Configuration:**
    *   `PROJECT_ID`, `LOCATION`, `VERTEX_AI_LOCATION`, `MODEL_NAME`:  **Crucially, you must replace these placeholders with your actual Google Cloud project ID, Dialogflow CX Agent location, Vertex AI Location and Gemini model name.**  The `VERTEX_AI_LOCATION` is the region where Vertex AI and Gemini are available. It's not necessarily the same as the Dialogflow CX `LOCATION`.
    *   `jobDetails`: Contains the job description.  This is the contextual information used by Gemini.
3.  **`generateAnswerWithGemini(question, jobDetails)`:**
    *   Initializes Vertex AI client using your `PROJECT_ID` and `VERTEX_AI_LOCATION`.
    *   Constructs a prompt for Gemini.  This is *very* important.  The prompt tells Gemini what role to play (a helpful job answering assistant), provides the job details as context, and then asks the candidate's question.  A well-crafted prompt is key to getting good results.  The prompt includes explicit instructions to be concise and handle cases where the question can't be answered from the provided context.
    *   Calls the Gemini API (`model.generateContentStream()`).
    *   Returns the generated answer.
    *   Includes error handling.
4.  **`dialogflowCXWebhook(req, res)`:**
    *   This is the main Cloud Functions function that gets triggered by Dialogflow CX.
    *   **Extracts information from the Dialogflow CX request:**
        *   `queryText`:  **IMPORTANT:**  This now uses `req.body.fulfillmentInfo.tag`.  This is the *fulfillment tag* you will set in your Dialogflow CX flow when you want to trigger the Gemini response.  For example, you would set the tag to "ask\_gemini" on the route that leads to this webhook.  This is much more robust than relying on intent names.
        *   `parameters`:  Accesses the Dialogflow CX session parameters using `req.body.sessionInfo.parameters`.
        *   `candidateQuestion`:  Retrieves the actual question the candidate asked. It assumes this question is stored in a Dialogflow CX parameter named `candidate_question`. **You need to define this parameter in your Dialogflow CX flow.**
    *   **Conditional Execution:** The `if (queryText === 'ask_gemini')` block ensures that the Gemini logic is only executed when the specific fulfillment tag is present in the request, preventing unintended calls to the AI model.
    *   **Calls `generateAnswerWithGemini()`:** Passes the question and job details to the Gemini function.
    *   **Constructs the Dialogflow CX response:**  The `responseData` object is formatted correctly for Dialogflow CX. It includes the Gemini-generated answer. You can also include `parameterChanges` to update the session context in Dialogflow CX if needed.
    *   **Sends the response back to Dialogflow CX:** The `res.status(200).send(responseData)` sends the properly formatted JSON response back to Dialogflow CX.
    *   **Error Handling:**  Includes a `try...catch` block to handle errors during the entire process and sends an error response to Dialogflow CX if something goes wrong.  The error messages are more specific now.
    *  **Default Response**  If the `queryText` (fulfillment tag) is not 'ask\_gemini', the function sends an empty JSON response `res.status(200).send({});`.  This is crucial.  It tells Dialogflow CX to continue with its normal flow and *not* to display an empty or error message.  This way, the webhook only intervenes when the specific "ask\_gemini" tag is present.

5.  **`resetDialogflowCXContext()`:** This is an *optional* function that shows how to reset the Dialogflow CX context (session parameters). You might use this during testing to clear the session.  It's not directly used in the main webhook logic, but it can be helpful for development.

**Deployment to Cloud Functions:**

1.  **Create a Cloud Functions Project:**  If you don't already have one, create a Google Cloud project.
2.  **Enable the Cloud Functions API:**  Enable the Cloud Functions API in your project.
3.  **Install the gcloud CLI:**  Install the Google Cloud SDK (gcloud CLI) on your machine: [https://cloud.google.com/sdk/docs/install](https://cloud.google.com/sdk/docs/install)
4.  **Authenticate the gcloud CLI:**  Authenticate with your Google Cloud account: `gcloud auth login`
5.  **Set the project:**  Set the current project: `gcloud config set project YOUR_PROJECT_ID`
6.  **Deploy the function:**
    *   Save the code above as `index.js`.
    *   Create a `package.json` file in the same directory with the following content:

    ```json
    {
      "name": "dialogflow-cx-webhook",
      "version": "1.0.0",
      "description": "Dialogflow CX webhook for Gemini integration",
      "main": "index.js",
      "scripts": {
        "start": "node index.js"
      },
      "dependencies": {
        "@google-cloud/vertexai": "^3.3.0",
        "@google-cloud/dialogflow-cx": "^4.2.0"
      }
    }
    ```
    *   Deploy the function using the gcloud CLI:

    ```bash
    gcloud functions deploy dialogflowCXWebhook \
      --runtime nodejs20 \
      --trigger-http \
      --region YOUR_REGION \
      --allow-unauthenticated
    ```

    Replace `YOUR_REGION` with the region where you want to deploy the function (e.g., `us-central1`).  Make sure it aligns with your Dialogflow CX agent's location. **Important: Your Vertex AI location may be different.**

7.  **Get the Cloud Functions URL:** After deployment, the gcloud CLI will output the URL of your Cloud Function.  You'll need this for the Dialogflow CX webhook configuration.
8.  **IAM Permissions:** The Cloud Function will use the default service account. Ensure that the service account has the following roles:
    *   `roles/dialogflow.agentUser` (Required for Dialogflow CX interaction)
    *   `roles/aiplatform.user` (Required for accessing Vertex AI / Gemini)

    You can grant these roles in the Google Cloud Console under IAM.  If you're using a custom service account, grant the roles to that account instead.
9. **API Enablement:** Verify that the Vertex AI API is enabled in your Google Cloud project. This is separate from the Cloud Functions API.

**Configuring the Webhook in Dialogflow CX:**

1.  **Open your Dialogflow CX Agent:** Go to the Dialogflow CX console.
2.  **Create a Route that calls the Webhook:**
    *   Create a new route in your Dialogflow CX flow (or edit an existing one).  This route should be triggered when you want to use the Gemini-powered response.
    *   **Define the route's condition:** The route's condition could be based on a specific intent being matched (e.g., an intent called "FallbackQuestion"). However, a more flexible approach is to use the fulfillment tag.
    *   **Set the Fulfillment Tag:** In the route's fulfillment, under "Advanced options," set the "Tag" field to `ask_gemini`.  This is the tag that will trigger the Gemini response in the webhook.
    *   **Add a Parameter:** In your Dialogflow CX flow, make sure you capture the candidate's question into a session parameter. Let's say you name this parameter `candidate_question`. The fulfillment tag works independently of the parameter.
3.  **Enable Webhook:** In the route's fulfillment, enable the webhook.
4.  **Enter the Cloud Functions URL:** Enter the URL of your deployed Cloud Function in the webhook configuration.

**Testing:**

1.  In the Dialogflow CX simulator, trigger the route you configured.  Ask a question that would fall outside the normal recruitment flow.
2.  Check the Cloud Functions logs in the Google Cloud Console to see the request and response data.  This is very helpful for debugging.
3.  Verify that the response from Dialogflow CX includes the Gemini-generated answer.
4.  Test different questions to see how Gemini responds and adjust the prompt in the `generateAnswerWithGemini` function as needed to improve the quality of the answers.

**Important Considerations and Improvements:**

*   **Security:**  Be mindful of security best practices for Cloud Functions. Consider using authentication and authorization mechanisms if your webhook requires sensitive data.
*   **Cost:**  Be aware that using Generative AI models can incur costs. Monitor your usage and optimize your prompts to reduce costs.
*   **Prompt Engineering:** The quality of the Gemini-generated answers depends heavily on the prompt. Experiment with different prompts to find the best approach for your use case. You can include examples of good answers in the prompt to guide Gemini.
*   **Context Management:** Carefully manage the Dialogflow CX session context. Use parameters to store information that is relevant to the conversation and pass it to the webhook.
*   **Fallback:** Implement a fallback mechanism in case the Gemini API fails or cannot provide a satisfactory answer.  You could provide a default response or redirect the user to a human agent.
*   **Error Handling:** The provided error handling is basic.  Enhance it with more detailed logging and monitoring to help you troubleshoot issues. Consider using a dedicated error tracking service.
*   **Model Selection:** Experiment with different Gemini models to find the one that best suits your needs. Some models may be more accurate or faster than others.
*  **Parameter Validation:** Before passing the `candidate_question` to Gemini, validate that it's not empty or malicious. This helps prevent errors and security vulnerabilities.
* **Session ID:** You can use the session ID (available in the request body) to track conversations and potentially store conversation history for better context.  Be mindful of data privacy regulations when storing user data.
* **API Keys:** Never hardcode API keys directly in your code. Use environment variables or Google Cloud Secret Manager to store API keys securely.

This comprehensive guide provides a solid foundation for building a Dialogflow CX webhook that leverages Google's Gemini AI for enhanced conversational experiences. Remember to adapt the code and configuration to your specific requirements and thoroughly test your implementation.
