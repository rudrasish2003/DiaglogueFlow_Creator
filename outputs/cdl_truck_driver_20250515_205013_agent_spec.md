```json
{
  "agent": {
    "displayName": "FedEx CDL Driver Recruitment Agent",
    "defaultLanguageCode": "en",
    "timeZone": "America/Chicago"
  },
  "flows": [
    {
      "name": "Default Start Flow",
      "transitionRoutes": [
        {
          "intent": "Default Welcome Intent",
          "targetPage": "Welcome Page"
        }
      ],
      "eventHandlers": [],
      "pages": [
        {
          "name": "Welcome Page",
          "displayName": "Welcome Page",
          "entryFulfillment": {
            "messages": [
              {
                "text": {
                  "text": [
                    "Hi, this is RecruitAI from FedEx. This call is regarding the CDL truck driver position at FedEx you applied for. Is this a good time to talk about it?"
                  ]
                }
              }
            ]
          },
          "form": {
            "parameters": [
              {
                "displayName": "good_time",
                "required": true,
                "entityType": "@yes_no",
                "fillBehavior": {
                  "initialPromptFulfillment": {
                    "messages": [
                      {
                        "text": {
                          "text": [
                            "Is this a good time to talk?"
                          ]
                        }
                      }
                    ]
                  }
                }
              }
            ]
          },
          "transitionRoutes": [
            {
              "condition": "$page.params.good_time.resolved == true",
              "targetPage": "Interest Confirmation Page"
            },
            {
              "condition": "$page.params.good_time.resolved == false",
              "fulfillment": {
                "messages": [
                  {
                    "text": {
                      "text": [
                        "No problem.  We can reschedule the call. What would be a better time for you?"
                      ]
                    }
                  }
                ]
              },
              "targetPage": "-"
            }
          ]
        },
        {
          "name": "Interest Confirmation Page",
          "displayName": "Interest Confirmation Page",
          "entryFulfillment": {
            "messages": [
              {
                "text": {
                  "text": [
                    "Are you still interested in the position?"
                  ]
                }
              }
            ]
          },
          "form": {
            "parameters": [
              {
                "displayName": "is_interested",
                "required": true,
                "entityType": "@yes_no",
                "fillBehavior": {
                  "initialPromptFulfillment": {
                    "messages": [
                      {
                        "text": {
                          "text": [
                            "Are you interested in the CDL truck driver position?"
                          ]
                        }
                      }
                    ]
                  }
                }
              }
            ]
          },
          "transitionRoutes": [
            {
              "condition": "$page.params.is_interested.resolved == true",
              "targetPage": "Name Confirmation Page"
            },
            {
              "condition": "$page.params.is_interested.resolved == false",
              "fulfillment": {
                "messages": [
                  {
                    "text": {
                      "text": [
                        "Thank you for your time. We'll remove you from consideration for this position."
                      ]
                    }
                  }
                ]
              },
              "targetPage": "-"
            }
          ]
        },
        {
          "name": "Name Confirmation Page",
          "displayName": "Name Confirmation Page",
          "entryFulfillment": {
            "messages": [
              {
                "text": {
                  "text": [
                    "Great! Could you confirm your name for our records?"
                  ]
                }
              }
            ]
          },
          "form": {
            "parameters": [
              {
                "displayName": "candidate_name",
                "required": true,
                "entityType": "@sys.person",
                "fillBehavior": {
                  "initialPromptFulfillment": {
                    "messages": [
                      {
                        "text": {
                          "text": [
                            "Please provide your full name."
                          ]
                        }
                      }
                    ]
                  }
                }
              }
            ]
          },
          "transitionRoutes": [
            {
              "condition": "$page.params.candidate_name.resolved != null",
              "targetPage": "Previous Experience Check Page"
            }
          ]
        },
        {
          "name": "Previous Experience Check Page",
          "displayName": "Previous Experience Check Page",
          "entryFulfillment": {
            "messages": [
              {
                "text": {
                  "text": [
                    "Have you worked for FedEx before?"
                  ]
                }
              }
            ]
          },
          "form": {
            "parameters": [
              {
                "displayName": "worked_for_company",
                "required": true,
                "entityType": "@yes_no",
                "fillBehavior": {
                  "initialPromptFulfillment": {
                    "messages": [
                      {
                        "text": {
                          "text": [
                            "Have you previously been employed by FedEx?"
                          ]
                        }
                      }
                    ]
                  }
                }
              }
            ]
          },
          "transitionRoutes": [
            {
              "condition": "$page.params.worked_for_company.resolved == true",
              "targetPage": "Position Check Page"
            },
            {
              "condition": "$page.params.worked_for_company.resolved == false",
              "targetPage": "Qualification Check 1 Page"
            }
          ]
        },
        {
          "name": "Qualification Check 1 Page",
          "displayName": "Qualification Check 1 Page",
          "entryFulfillment": {
            "messages": [
              {
                "text": {
                  "text": [
                    "Do you have a minimum of 1 year of verifiable OTR experience?"
                  ]
                }
              }
            ]
          },
          "form": {
            "parameters": [
              {
                "displayName": "has_qualification_1",
                "required": true,
                "entityType": "@yes_no",
                "fillBehavior": {
                  "initialPromptFulfillment": {
                    "messages": [
                      {
                        "text": {
                          "text": [
                            "Please confirm you have at least one year of over-the-road (OTR) experience as a truck driver."
                          ]
                        }
                      }
                    ]
                  }
                }
              }
            ]
          },
          "transitionRoutes": [
            {
              "condition": "$page.params.has_qualification_1.resolved == true",
              "targetPage": "Qualification Check 2 Page"
            },
            {
              "condition": "$page.params.has_qualification_1.resolved == false",
              "fulfillment": {
                "messages": [
                  {
                    "text": {
                      "text": [
                        "Unfortunately, this position requires at least one year of OTR experience. Thank you for your time."
                      ]
                    }
                  }
                ]
              },
              "targetPage": "-"
            }
          ]
        },
        {
          "name": "Qualification Check 2 Page",
          "displayName": "Qualification Check 2 Page",
          "entryFulfillment": {
            "messages": [
              {
                "text": {
                  "text": [
                    "Are you at least 23 years old?"
                  ]
                }
              }
            ]
          },
          "form": {
            "parameters": [
              {
                "displayName": "meets_age_requirement",
                "required": true,
                "entityType": "@yes_no",
                "fillBehavior": {
                  "initialPromptFulfillment": {
                    "messages": [
                      {
                        "text": {
                          "text": [
                            "Please confirm that you are at least 23 years of age."
                          ]
                        }
                      }
                    ]
                  }
                }
              }
            ]
          },
          "transitionRoutes": [
            {
              "condition": "$page.params.meets_age_requirement.resolved == true",
              "targetPage": "Transportation Check Page"
            },
            {
              "condition": "$page.params.meets_age_requirement.resolved == false",
              "fulfillment": {
                "messages": [
                  {
                    "text": {
                      "text": [
                        "You must be at least 23 years old to qualify. Thank you for your time."
                      ]
                    }
                  }
                ]
              },
              "targetPage": "-"
            }
          ]
        },
        {
          "name": "Transportation Check Page",
          "displayName": "Transportation Check Page",
          "entryFulfillment": {
            "messages": [
              {
                "text": {
                  "text": [
                    "Do you have reliable transportation to get to the job every day, within the Midwest (within 500 miles of Chicago)?"
                  ]
                }
              }
            ]
          },
          "form": {
            "parameters": [
              {
                "displayName": "has_transportation",
                "required": true,
                "entityType": "@yes_no",
                "fillBehavior": {
                  "initialPromptFulfillment": {
                    "messages": [
                      {
                        "text": {
                          "text": [
                            "Do you have a dependable way to travel to work each day, to the Chicago area?"
                          ]
                        }
                      }
                    ]
                  }
                }
              }
            ]
          },
          "transitionRoutes": [
            {
              "condition": "$page.params.has_transportation.resolved == true",
              "targetPage": "Current Employment Page"
            },
            {
              "condition": "$page.params.has_transportation.resolved == false",
              "fulfillment": {
                "messages": [
                  {
                    "text": {
                      "text": [
                        "Unfortunately, reliable transportation is required.  Thank you for your time."
                      ]
                    }
                  }
                ]
              },
              "targetPage": "-"
            }
          ]
        },
        {
          "name": "Current Employment Page",
          "displayName": "Current Employment Page",
          "entryFulfillment": {
            "messages": [
              {
                "text": {
                  "text": [
                    "Where are you currently working and why are you looking to make a change?"
                  ]
                }
              }
            ]
          },
          "form": {
            "parameters": [
              {
                "displayName": "current_employer",
                "required": true,
                "entityType": "@sys.any",
                "fillBehavior": {
                  "initialPromptFulfillment": {
                    "messages": [
                      {
                        "text": {
                          "text": [
                            "What is your current employer?"
                          ]
                        }
                      }
                    ]
                  }
                }
              },
              {
                "displayName": "reason_for_change",
                "required": true,
                "entityType": "@sys.any",
                "fillBehavior": {
                  "initialPromptFulfillment": {
                    "messages": [
                      {
                        "text": {
                          "text": [
                            "Why are you looking for a new job?"
                          ]
                        }
                      }
                    ]
                  }
                }
              }
            ]
          },
          "transitionRoutes": [
            {
              "condition": "$page.params.current_employer.resolved != null && $page.params.reason_for_change.resolved != null",
              "targetPage": "Background Check Page"
            }
          ]
        },
        {
          "name": "Background Check Page",
          "displayName": "Background Check Page",
          "entryFulfillment": {
            "messages": [
              {
                "text": {
                  "text": [
                    "Will you be able to pass a background verification check?"
                  ]
                }
              }
            ]
          },
          "form": {
            "parameters": [
              {
                "displayName": "can_pass_checks",
                "required": true,
                "entityType": "@yes_no",
                "fillBehavior": {
                  "initialPromptFulfillment": {
                    "messages": [
                      {
                        "text": {
                          "text": [
                            "Please confirm that you will pass a background check."
                          ]
                        }
                      }
                    ]
                  }
                }
              }
            ]
          },
          "transitionRoutes": [
            {
              "condition": "$page.params.can_pass_checks.resolved == true",
              "targetPage": "Conclusion Page"
            },
            {
              "condition": "$page.params.can_pass_checks.resolved == false",
              "fulfillment": {
                "messages": [
                  {
                    "text": {
                      "text": [
                        "Passing a background check is required for this position. Thank you for your time."
                      ]
                    }
                  }
                ]
              },
              "targetPage": "-"
            }
          ]
        },
        {
          "name": "Conclusion Page",
          "displayName": "Conclusion Page",
          "entryFulfillment": {
            "messages": [
              {
                "text": {
                  "text": [
                    "Thank you for your time. Based on our conversation, we'll be in touch regarding next steps. Do you have any questions for me?"
                  ]
                }
              }
            ]
          },
          "transitionRoutes": [
            {
              "intent": "Default Fallback Intent",
              "targetPage": "Candidate Question Fallback Page"
            },
            {
              "intent": "actions.confirmation.yes",
              "fulfillment": {
                "messages": [
                  {
                    "text": {
                      "text": [
                        "Thanks you for your time, we will be in touch!"
                      ]
                    }
                  }
                ]
              },
              "targetPage": "-"
            },
            {
              "intent": "actions.confirmation.no",
              "fulfillment": {
                "messages": [
                  {
                    "text": {
                      "text": [
                        "Thanks you for your time, we will be in touch!"
                      ]
                    }
                  }
                ]
              },
              "targetPage": "-"
            }
          ]
        },
        {
          "name": "Position Check Page",
          "displayName": "Position Check Page",
          "entryFulfillment": {
            "messages": [
              {
                "text": {
                  "text": [
                    "Thank you for confirming. We already have your employment data on file. Because of this, all that we need to confirm is your current employment preferences. Do you still have interest in the cdl truck driver position?"
                  ]
                }
              }
            ]
          },
          "form": {
            "parameters": [
              {
                "displayName": "confirm_interest",
                "required": true,
                "entityType": "@yes_no",
                "fillBehavior": {
                  "initialPromptFulfillment": {
                    "messages": [
                      {
                        "text": {
                          "text": [
                            "Confirm that you still want the truck driving position?"
                          ]
                        }
                      }
                    ]
                  }
                }
              }
            ]
          },
          "transitionRoutes": [
            {
              "condition": "$page.params.confirm_interest.resolved == true",
              "targetPage": "Transportation Check Page"
            },
            {
              "condition": "$page.params.confirm_interest.resolved == false",
              "fulfillment": {
                "messages": [
                  {
                    "text": {
                      "text": [
                        "Ok, thanks for your time."
                      ]
                    }
                  }
                ]
              },
              "targetPage": "-"
            }
          ]
        },
        {
          "name": "Candidate Question Fallback Page",
          "displayName": "Candidate Question Fallback Page",
          "entryFulfillment": {
            "messages": [
              {
                "text": {
                  "text": [
                    "One moment, let me look that up for you..."
                  ]
                }
              }
            ],
            "webhook": "answer_candidate_question"
          },
          "transitionRoutes": [
            {
              "condition": "$session.params.llm_response != null",
              "fulfillment": {
                "messages": [
                  {
                    "text": {
                      "text": [
                        "$session.params.llm_response"
                      ]
                    }
                  }
                ]
              },
              "targetPage": "Conclusion Page"
            }
          ],
          "eventHandlers": [
            {
              "event": "NO_MATCH",
              "triggerFulfillment": {
                "messages": [
                  {
                    "text": {
                      "text": [
                        "Sorry, I didn't understand.  Please clarify your question."
                      ]
                    }
                  }
                ]
              },
              "repeatEventCountLimit": 1,
              "targetPage": "Candidate Question Fallback Page"
            },
            {
              "event": "NO_INPUT",
              "triggerFulfillment": {
                "messages": [
                  {
                    "text": {
                      "text": [
                        "Please ask your question."
                      ]
                    }
                  }
                ]
              },
              "repeatEventCountLimit": 1,
              "targetPage": "Candidate Question Fallback Page"
            }
          ]
        }
      ]
    }
  ],
  "intents": [
    {
      "name": "Default Welcome Intent",
      "trainingPhrases": [
        "Hi",
        "Hello",
        "Good morning",
        "Good afternoon",
        "Hey there"
      ]
    },
    {
      "name": "actions.confirmation.yes",
      "trainingPhrases": [
        "yes",
        "yeah",
        "indeed"
      ]
    },
    {
      "name": "actions.confirmation.no",
      "trainingPhrases": [
        "no",
        "nope",
        "nah"
      ]
    }
  ],
  "entityTypes": [
    {
      "name": "yes_no",
      "kind": "KIND_MAP",
      "entities": [
        {
          "value": "yes",
          "synonyms": [
            "yes",
            "yeah",
            "yep",
            "sure",
            "absolutely",
            "definitely",
            "of course",
            "ok",
            "okay",
            "affirmative"
          ]
        },
        {
          "value": "no",
          "synonyms": [
            "no",
            "nope",
            "nah",
            "not",
            "never",
            "absolutely not",
            "definitely not"
          ]
        }
      ]
    }
  ],
  "webhooks": [
    {
      "name": "answer_candidate_question",
      "displayName": "AnswerCandidateQuestion",
      "genericService": {
        "uri": "YOUR_LLM_WEBHOOK_ENDPOINT",
        "httpMethod": "POST",
        "requestBody": {
          "question": "$request.intent.queryInfo.query"
        },
        "requestHeaders": {
          "Content-Type": "application/json"
        },
        "responseHeaders": [],
        "isCloudFunctionsIntegrated": false
      },
      "timeout": "30.0s",
      "disabled": false,
      "conditionalCases": []
    }
  ]
}
```

**Explanation and Key Improvements:**

1. **Detailed Conversation Flow:** The specification follows the provided conversation structure precisely.  Each page is defined with its entry fulfillment (the message spoken to the user), form parameters (data collected from the user), and transition routes (logic to move to the next page based on the user's responses).

2. **Industry-Specific Parameters Integrated:** The `qualification_1` and `age_requirement` values are dynamically inserted into the appropriate pages.

3.  **Job Details Usage:**  Job details from provided spec are used in several spots, like including the location and the type of driving to be done in the transportation check page.

4. **Entity Definitions:**  The `yes_no` entity is defined with a comprehensive list of synonyms. This makes the agent more robust in understanding user responses.

5. **Parameter Definitions:** Each parameter is defined with its `displayName`, `entityType`, `required` flag, and `fillBehavior`.  The `fillBehavior` ensures that the agent prompts the user until the parameter is filled.

6. **Natural Conversational Fulfillment:**  The fulfillment messages are designed to sound more natural and less robotic. For example, "No problem. We can reschedule the call. What would be a better time for you?" is more conversational than simply saying "Okay."

7. **Fallback Handling for Candidate Questions (CRITICAL):**

   *   **`Candidate Question Fallback Page`:**  This new page is triggered by the `Default Fallback Intent`. This ensures that *any* question the user asks that isn't explicitly covered by the flow gets routed to this page.
   *   **Webhook Integration:** This page uses a webhook called `answer_candidate_question`.  This webhook POSTs the user's question (`$request.intent.queryInfo.query`) to a specified URL (`YOUR_LLM_WEBHOOK_ENDPOINT`). You need to replace this placeholder with the actual URL of your LLM endpoint.
   *   **LLM Response Handling:** The response from the LLM is stored in the `$session.params.llm_response` session parameter. The transition route then displays this response to the user.
   *   **Context Management:** Critically, *after* the LLM answers the question, the `Conclusion Page` is the target page. This is so that the conversation resumes.
   *   **No Match and No Input Event Handlers**: To reduce the potential for infinite loops, both the NO_MATCH and NO_INPUT event handlers prompt the user to ask their question again, instead of defaulting straight to the LLM, in case of a misinterpretation.
   *  **Reasonable LLM parameters:** The webhook request body shows that a question parameter will be used for the prompt. This should be used in the LLM prompt, as well as providing the details about the job.

8. **Webhook Payload Example (for your LLM endpoint):**

   The LLM endpoint will receive a JSON payload like this:

   ```json
   {
     "question": "What is the starting salary?"
   }
   ```

   Your LLM endpoint must then generate a response string and return it as JSON. For example:

   ```json
   {
     "answer": "The pay rate is $0.58-$0.65 per mile based on experience; average weekly miles: 2,500-3,000; Weekly pay with direct deposit."
   }
   ```

   The Dialogflow CX agent then picks this `answer` up and displays it to the user. *Make sure your LLM returns the answer in a JSON format with a key called `answer`.* The Dialogflow CX agent relies on this. Your webhook needs to return a result in this format:

   ```json
   {
       "fulfillment_response": {
           "messages": [
               {
                   "text": {
                       "text": [
                           "Your Answer"
                       ]
                   }
               }
           ]
       }
   }
   ```

9. **LLM Prompt Guidance:**

   When your LLM receives the `question`, construct a prompt like this:

   ```
   You are a helpful and informative recruitment agent for FedEx. Answer the candidate's question based on the following job information:

   Position: CDL Truck Driver
   Company: FedEx
   Requirements: Valid Class A Commercial Driver's License, Clean MVR with no more than 2 moving violations in the past 3 years, No DUIs or reckless driving convictions, Must be at least 23 years of age, Must pass DOT physical and drug screen, Able to lift up to 50 lbs occasionally, High school diploma or GED preferred
   Pay: $0.58-$0.65 per mile based on experience; average weekly miles: 2,500-3,000; Weekly pay with direct deposit
   Schedule: Regional routes with 2-3 nights home per week; Consistent freight - no seasonal layoffs
   Benefits: Sign-on bonus: $3,000 (paid in installments), Safety bonuses up to $500 quarterly, Medical, dental, and vision insurance after 60 days, 401(k) with 3% company match after 90 days, Paid vacation (1 week after first year), Paid holidays, Referral bonuses: $1,500 per hired driver, Newer equipment with latest safety features
   Location: Midwest, within 500-mile radius of Chicago terminal

   Question: {candidate_question}

   Answer:
   ```

   Replace `{candidate_question}` with the actual question from the user.  This provides the LLM with the necessary context to answer the question accurately.

10. **Comprehensive Training Phrases:** Example training phrases for "yes" and "no" are included, improving the agent's understanding of user intents.

**Important Considerations:**

*   **Replace `YOUR_LLM_WEBHOOK_ENDPOINT`:**  You *must* replace this placeholder with the actual URL of your LLM endpoint.
*   **LLM Endpoint Implementation:** You need to implement the LLM endpoint to receive the question, construct a prompt, query the LLM, and return the answer in the correct JSON format.
*   **Thorough Testing:** Test the agent thoroughly with a wide range of questions and responses to ensure it functions correctly.
*   **Error Handling:**  Implement error handling in your LLM endpoint to gracefully handle cases where the LLM cannot answer the question or encounters an error. You can then send an appropriate error message back to the Dialogflow CX agent.
*   **Security:** Secure your LLM endpoint appropriately.
*  **Monitor Performance**:  Continuously monitor the agent's performance and user feedback to identify areas for improvement.
*   **Data Privacy**: Ensure compliance with all data privacy regulations when collecting and processing user data.
