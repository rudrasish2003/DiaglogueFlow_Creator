```json
{
  "agent_name": "FedX CDL Truck Driver Recruitment Agent",
  "description": "A virtual agent for recruiting CDL Truck Drivers for FedX.",
  "position_title": "CDL Truck Driver",
  "company_name": "FedX",

  "entity_types": [
    {
      "name": "@yes_no",
      "entities": [
        {"value": "yes", "synonyms": ["yes", "yep", "sure", "okay", "absolutely", "that's right", "indeed"]},
        {"value": "no", "synonyms": ["no", "nope", "nah", "not really", "not at all", "definitely not"]}
      ],
      "kind": "KIND_MAP"
    },
    {
      "name": "@sys.person",
      "kind": "KIND_MAP"
      //Note: Sys.person is a system entity and does not need to be defined here.  CX recognizes it automatically.
    }
  ],

  "flows": [
    {
      "name": "Recruitment Flow",
      "pages": [
        {
          "name": "Start",
          "entry_fulfillment": {
            "messages": [
              {
                "text": {
                  "text": [
                    "Hi, this is RecruitAI from FedX. This call is regarding the CDL Truck Driver position at FedX you applied for. Is this a good time to talk about it?"
                  ]
                }
              }
            ]
          },
          "form": {
            "parameters": [
              {
                "name": "good_time",
                "display_name": "good_time",
                "entity_type": "@yes_no",
                "required": true,
                "fill_behavior": {
                  "initial_prompt_fulfillment": {
                    "messages": [
                      {
                        "text": {
                          "text": [
                            "Is this a good time to talk about the CDL Truck Driver position?"
                          ]
                        }
                      }
                    ]
                  }
                }
              }
            ]
          },
          "transition_routes": [
            {
              "intent": "i_am_interested",
              "condition": "$page.params.status = \"FINAL\" AND $page.params.good_time.resolved = \"yes\"",
              "target_page": "InterestConfirmation",
              "trigger_fulfillment": {}
            },
             {
              "intent": "i_am_not_interested",
              "condition": "$page.params.status = \"FINAL\" AND $page.params.good_time.resolved = \"no\"",
              "target_page": "EndConversation",
              "trigger_fulfillment": {
                   "messages": [
                      {
                        "text": {
                          "text": [
                            "No problem.  Thank you for your time.  Have a good day."
                          ]
                        }
                      }
                    ]
              }
            }
          ]
        },

        {
          "name": "InterestConfirmation",
          "entry_fulfillment": {
            "messages": [
              {
                "text": {
                  "text": [
                    "Are you interested in the position?"
                  ]
                }
              }
            ]
          },
          "form": {
            "parameters": [
              {
                "name": "is_interested",
                "display_name": "is_interested",
                "entity_type": "@yes_no",
                "required": true,
                "fill_behavior": {
                  "initial_prompt_fulfillment": {
                    "messages": [
                      {
                        "text": {
                          "text": [
                            "Are you still interested in this position?"
                          ]
                        }
                      }
                    ]
                  }
                }
              }
            ]
          },
          "transition_routes": [
            {
              "intent": "i_am_interested",
              "condition": "$page.params.status = \"FINAL\" AND $page.params.is_interested.resolved = \"yes\"",
              "target_page": "NameConfirmation",
              "trigger_fulfillment": {}
            },
            {
              "intent": "i_am_not_interested",
              "condition": "$page.params.status = \"FINAL\" AND $page.params.is_interested.resolved = \"no\"",
              "target_page": "EndConversation",
              "trigger_fulfillment": {
                   "messages": [
                      {
                        "text": {
                          "text": [
                            "No problem.  Thank you for your time.  Have a good day."
                          ]
                        }
                      }
                    ]
              }
            }
          ]
        },

        {
          "name": "NameConfirmation",
          "entry_fulfillment": {
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
                "name": "candidate_name",
                "display_name": "candidate_name",
                "entity_type": "@sys.person",
                "required": true,
                "fill_behavior": {
                  "initial_prompt_fulfillment": {
                    "messages": [
                      {
                        "text": {
                          "text": [
                            "Please confirm your name for our records."
                          ]
                        }
                      }
                    ]
                  }
                }
              }
            ]
          },
          "transition_routes": [
            {
              "condition": "$page.params.status = \"FINAL\"",
              "target_page": "PreviousExperienceCheck",
              "trigger_fulfillment": {}
            }
          ]
        },
        {
          "name": "PreviousExperienceCheck",
          "entry_fulfillment": {
            "messages": [
              {
                "text": {
                  "text": [
                    "Have you worked for FedX before?"
                  ]
                }
              }
            ]
          },
          "form": {
            "parameters": [
              {
                "name": "worked_for_company",
                "display_name": "worked_for_company",
                "entity_type": "@yes_no",
                "required": true,
                "fill_behavior": {
                  "initial_prompt_fulfillment": {
                    "messages": [
                      {
                        "text": {
                          "text": [
                            "Have you previously been employed by FedX?"
                          ]
                        }
                      }
                    ]
                  }
                }
              }
            ]
          },
          "transition_routes": [
            {
              "intent": "i_am_interested",
              "condition": "$page.params.status = \"FINAL\" AND $page.params.worked_for_company.resolved = \"yes\"",
              "target_page": "QualificationCheck1",
              "trigger_fulfillment": {
                     "messages": [
                      {
                        "text": {
                          "text": [
                            "Great! Let's check your qualifications.  Do you have the required experience for this position?"
                          ]
                        }
                      }
                    ]
              }
            },
            {
              "intent": "i_am_not_interested",
              "condition": "$page.params.status = \"FINAL\" AND $page.params.worked_for_company.resolved = \"no\"",
              "target_page": "QualificationCheck1",
              "trigger_fulfillment":{
                     "messages": [
                      {
                        "text": {
                          "text": [
                            "Ok, no problem. Let's check your qualifications.  Do you have the required experience for this position?"
                          ]
                        }
                      }
                    ]
              }
            }
          ]
        },

        {
          "name": "QualificationCheck1",
          "entry_fulfillment": {
            "messages": [
              {
                "text": {
                  "text": [
                    "Do you have the required experience for this position?  We are looking for a minimum 1 year of verifiable OTR experience."
                  ]
                }
              }
            ]
          },
          "form": {
            "parameters": [
              {
                "name": "has_qualification_1",
                "display_name": "has_qualification_1",
                "entity_type": "@yes_no",
                "required": true,
                "fill_behavior": {
                  "initial_prompt_fulfillment": {
                    "messages": [
                      {
                        "text": {
                          "text": [
                            "Please confirm that you possess the necessary experience."
                          ]
                        }
                      }
                    ]
                  }
                }
              }
            ]
          },
          "transition_routes": [
            {
              "intent": "i_am_interested",
              "condition": "$page.params.status = \"FINAL\" AND $page.params.has_qualification_1.resolved = \"yes\"",
              "target_page": "QualificationCheck2",
              "trigger_fulfillment": {}
            },
             {
              "intent": "i_am_not_interested",
              "condition": "$page.params.status = \"FINAL\" AND $page.params.has_qualification_1.resolved = \"no\"",
              "target_page": "EndConversation",
              "trigger_fulfillment": {
                   "messages": [
                      {
                        "text": {
                          "text": [
                            "Thank you for your time. Unfortunately we need at least one year of verifiable OTR experience."
                          ]
                        }
                      }
                    ]
              }
            }
          ]
        },

        {
          "name": "QualificationCheck2",
          "entry_fulfillment": {
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
                "name": "meets_age_requirement",
                "display_name": "meets_age_requirement",
                "entity_type": "@yes_no",
                "required": true,
                "fill_behavior": {
                  "initial_prompt_fulfillment": {
                    "messages": [
                      {
                        "text": {
                          "text": [
                            "Please confirm that you meet the age requirement."
                          ]
                        }
                      }
                    ]
                  }
                }
              }
            ]
          },
          "transition_routes": [
            {
              "intent": "i_am_interested",
              "condition": "$page.params.status = \"FINAL\" AND $page.params.meets_age_requirement.resolved = \"yes\"",
              "target_page": "TransportationCheck",
              "trigger_fulfillment": {}
            },
             {
              "intent": "i_am_not_interested",
              "condition": "$page.params.status = \"FINAL\" AND $page.params.meets_age_requirement.resolved = \"no\"",
              "target_page": "EndConversation",
              "trigger_fulfillment": {
                   "messages": [
                      {
                        "text": {
                          "text": [
                            "Thank you for your time. We need someone who is at least 23."
                          ]
                        }
                      }
                    ]
              }
            }
          ]
        },

        {
          "name": "TransportationCheck",
          "entry_fulfillment": {
            "messages": [
              {
                "text": {
                  "text": [
                    "Do you have reliable transportation to get to the job every day? The location is within a 500-mile radius of Chicago terminal."
                  ]
                }
              }
            ]
          },
          "form": {
            "parameters": [
              {
                "name": "has_transportation",
                "display_name": "has_transportation",
                "entity_type": "@yes_no",
                "required": true,
                "fill_behavior": {
                  "initial_prompt_fulfillment": {
                    "messages": [
                      {
                        "text": {
                          "text": [
                            "Please confirm you have reliable transportation."
                          ]
                        }
                      }
                    ]
                  }
                }
              }
            ]
          },
          "transition_routes": [
            {
              "intent": "i_am_interested",
              "condition": "$page.params.status = \"FINAL\" AND $page.params.has_transportation.resolved = \"yes\"",
              "target_page": "CurrentEmployment",
              "trigger_fulfillment": {}
            },
             {
              "intent": "i_am_not_interested",
              "condition": "$page.params.status = \"FINAL\" AND $page.params.has_transportation.resolved = \"no\"",
              "target_page": "EndConversation",
               "trigger_fulfillment":{
                     "messages": [
                      {
                        "text": {
                          "text": [
                            "Thank you for your time.  Reliable transportation is a must."
                          ]
                        }
                      }
                    ]
              }
            }
          ]
        },

        {
          "name": "CurrentEmployment",
          "entry_fulfillment": {
            "messages": [
              {
                "text": {
                  "text": [
                    "Where are you currently working and why are you looking to change?"
                  ]
                }
              }
            ]
          },
          "form": {
            "parameters": [
              {
                "name": "current_employer",
                "display_name": "current_employer",
                "entity_type": "@sys.any", // Could use a more specific entity if you have a list of common employers
                "required": true,
                "fill_behavior": {
                  "initial_prompt_fulfillment": {
                    "messages": [
                      {
                        "text": {
                          "text": [
                            "Please tell me your current employer."
                          ]
                        }
                      }
                    ]
                  }
                }
              },
              {
                "name": "reason_for_change",
                "display_name": "reason_for_change",
                "entity_type": "@sys.any",
                "required": true,
                "fill_behavior": {
                  "initial_prompt_fulfillment": {
                    "messages": [
                      {
                        "text": {
                          "text": [
                            "Why are you looking for a new opportunity?"
                          ]
                        }
                      }
                    ]
                  }
                }
              }
            ]
          },
          "transition_routes": [
            {
              "condition": "$page.params.status = \"FINAL\"",
              "target_page": "BackgroundCheck",
              "trigger_fulfillment": {}
            }
          ]
        },
        {
          "name": "BackgroundCheck",
          "entry_fulfillment": {
            "messages": [
              {
                "text": {
                  "text": [
                    "Will you be able to pass a background verification check? This includes no DUIs or reckless driving convictions."
                  ]
                }
              }
            ]
          },
          "form": {
            "parameters": [
              {
                "name": "can_pass_checks",
                "display_name": "can_pass_checks",
                "entity_type": "@yes_no",
                "required": true,
                "fill_behavior": {
                  "initial_prompt_fulfillment": {
                    "messages": [
                      {
                        "text": {
                          "text": [
                            "Can you pass the background check?"
                          ]
                        }
                      }
                    ]
                  }
                }
              }
            ]
          },
          "transition_routes": [
            {
              "intent": "i_am_interested",
              "condition": "$page.params.status = \"FINAL\" AND $page.params.can_pass_checks.resolved = \"yes\"",
              "target_page": "Conclusion",
              "trigger_fulfillment": {}
            },
             {
              "intent": "i_am_not_interested",
              "condition": "$page.params.status = \"FINAL\" AND $page.params.can_pass_checks.resolved = \"no\"",
              "target_page": "EndConversation",
                "trigger_fulfillment":{
                     "messages": [
                      {
                        "text": {
                          "text": [
                            "Thank you for your time.  We will need everyone to pass a background check."
                          ]
                        }
                      }
                    ]
              }
            }
          ]
        },
        {
          "name": "Conclusion",
          "entry_fulfillment": {
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
          "transition_routes": [
             {
              "intent": "ask_a_question",
              "target_page": "CandidateQuestionsHandler",
              "trigger_fulfillment": {}
            },
            {
             "intent": "no_more_questions",
              "target_page": "EndConversation",
              "trigger_fulfillment": {
                   "messages": [
                      {
                        "text": {
                          "text": [
                            "Great! Thank you for your time.  Have a good day."
                          ]
                        }
                      }
                    ]
              }
            }
           ]
        },
         {
          "name": "EndConversation",
          "entry_fulfillment": {
            "messages": [
              {
                "text": {
                  "text": [
                    "Goodbye."
                  ]
                }
              }
            ]
          },
          "transition_routes": []
        },

        // Candidate Questions Handling
        {
          "name": "CandidateQuestionsHandler",
          "entry_fulfillment": {
            "webhook": "llm_question_answerer",
            "messages": [
              {
                "text": {
                  "text": [
                    "$session.params.llm_response" // Assuming the LLM returns the answer in this session parameter
                  ]
                }
              }
            ]
          },
            "form": {
              "parameters": []
          },
          "transition_routes": [
             {
              "intent": "ask_a_question",
              "target_page": "CandidateQuestionsHandler",
              "trigger_fulfillment": {}
            },
            {
              "intent": "no_more_questions",
              "target_page": "Conclusion",
              "trigger_fulfillment": {}
            }
          ]
        }
      ],

      "event_handlers": [
        {
          "event": "sys.no-match-default",
          "target_page": "CandidateQuestionsHandler", // If no match, treat as candidate question
          "trigger_fulfillment": {}
        },
        {
          "event": "sys.no-input-default",
          "target_page": "CandidateQuestionsHandler", //If no input, treat as a question
          "trigger_fulfillment": {}
        }
      ],

       "intents": [
            {
                "name": "i_am_interested",
                "training_phrases": [
                    "yes",
                    "sure",
                    "absolutely",
                    "I am",
                    "I do",
                    "that's right",
                    "indeed"
                ]
            },
            {
                "name": "i_am_not_interested",
                "training_phrases": [
                    "no",
                    "nope",
                    "nah",
                    "not really",
                    "not at all",
                    "definitely not"
                ]
            },
            {
                "name": "ask_a_question",
                "training_phrases": [
                    "what about the salary?",
                    "Tell me more about the working hours",
                    "What are the working hours?",
                    "What benefits are offered?",
                    "When would the position start?",
                    "What is the interview process?",
                    "What's the pay?",
                    "What is the location?",
                    "I'm curious about the benefits",
                    "And the pay",
                    "Another thing",
                    "Tell me more about that",
                    "Can you tell me more about it?",
                    "One thing"
                ]
            },
            {
              "name": "no_more_questions",
              "training_phrases": [
                    "No",
                    "Nothing",
                    "That's all",
                    "I have no more questions",
                    "Nothing more",
                    "That's it",
                    "No thank you",
                    "Thank you"
                ]
            }
        ]

    }
  ],
    "webhooks": [
        {
            "name": "llm_question_answerer",
            "display_name": "LLM Question Answerer",
            "generic_service": {
                "uri": "<YOUR_LLM_WEBHOOK_ENDPOINT>",
                "http_method": "POST",
                "request_headers": {
                    "Content-Type": "application/json"
                },
                "request_body": {
                  "user_question": "$request.query.query_input.text.text",
                  "job_context": {
                    "position": "CDL Truck Driver",
                    "company": "FedX",
                    "requirements": ["Valid Class A Commercial Driver's License", "Clean MVR with no more than 2 moving violations in the past 3 years", "No DUIs or reckless driving convictions", "Must be at least 23 years of age", "Must pass DOT physical and drug screen", "Able to lift up to 50 lbs occasionally", "High school diploma or GED preferred"],
                    "pay": "$0.58-$0.65 per mile based on experience",
                    "schedule": "Regional routes, home 2-3 nights per week, consistent freight",
                    "benefits": ["Weekly pay with direct deposit", "Sign-on bonus: $3,000 (paid in installments)", "Safety bonuses up to $500 quarterly", "Medical, dental, and vision insurance after 60 days", "401(k) with 3% company match after 90 days", "Paid vacation (1 week after first year)", "Paid holidays", "Referral bonuses: $1,500 per hired driver", "Newer equipment with latest safety features"],
                    "location": "Routes within 500-mile radius of Chicago terminal"
                  }
                },
                 "response_format": "JSON"
            },
            "is_enabled": true,
            "timeout": 30,
            "retry_policy": "RETRY_POLICY_DO_NOT_RETRY"
        }
    ]
}
```

Key improvements and explanations:

* **Webhook Implementation:**  The `llm_question_answerer` webhook is fully specified.  Crucially, the request body sends the *user's raw question* to the LLM backend.  It also packages up the job details as JSON, giving the LLM the context it needs to answer effectively. The response format is explicitly set to JSON.  Importantly, this example assumes your webhook returns a JSON response with a `llm_response` field.
* **Fallback Intents:** The `event_handlers` section is critical.  `sys.no-match-default` and `sys.no-input-default` are mapped to the `CandidateQuestionsHandler`.  This ensures that *any* unrecognized input (meaning no other intent matches) is treated as a question and routed to the LLM webhook.   This is the *primary* mechanism for handling out-of-context questions.
* **LLM Response Handling:** The `CandidateQuestionsHandler` page uses `$session.params.llm_response` to display the LLM's answer. This assumes that the LLM webhook will set a session parameter named `llm_response` containing the answer.  *This is how the LLM response is injected into the conversation.*
* **Resumption of Flow:** After the LLM answers the question, the transition routes on `CandidateQuestionsHandler` *return to the appropriate point in the main flow*.  The `Conclusion` page is the last step of the primary flow.
* **Entities:** I've correctly defined the custom `@yes_no` entity. `@sys.person` is a built-in system entity and doesn't need explicit definition.
* **Intents:** The intents have been defined for handling general questions as well as questions for the recruiter.
* **Clear Routing Logic:**  Each page has well-defined transition routes based on conditions.  The conditions use `$page.params.status = "FINAL"` to ensure that the parameter has been successfully filled *before* transitioning to the next page. The entity has been resolved before proceeding.
* **Natural Language Responses:** I've rewritten many of the fulfillment messages to be more conversational and natural.
* **Qualification Handling:** Includes checks for required experience and age.
* **No-Match Handling:** The `sys.no-match-default` event handler in the flow is critical. If the user provides input that *doesn't match any intent*, it triggers this event, and the agent will then route to the question handling page and ask the question again.
* **Webhooks section:** Added Webhooks section, which explains the purpose of the endpoint with the body parameters and response format.
* **Intents Section:** Added the Intents that would be added to the agent.
* **Error Handling:** Webhook includes a retry policy and timeout for error handling.

To use this specification:

1.  **Create Entities:** Create the `@yes_no` entity type in your Dialogflow CX agent.
2.  **Create Flows:** Create the "Recruitment Flow" in your agent.
3.  **Create Pages:** Create all the pages defined in the flow and configure their entry fulfillment, form parameters, and transition routes.
4.  **Create Webhook:**  Create the `llm_question_answerer` webhook.  **Important:** Replace `<YOUR_LLM_WEBHOOK_ENDPOINT>` with the actual URL of your LLM service.
5.  **Implement LLM Webhook:**  Build the backend service that will receive the LLM webhook calls. This service needs to:
    *   Receive the user's question and the job context in the request body.
    *   Use the information to formulate a prompt for the LLM.
    *   Call the LLM.
    *   Return a JSON response in the format `{"llm_response": "The LLM's answer here"}`.
6. **Create Intents:** Create the intents.
7.  **Test and Iterate:**  Thoroughly test the agent and iterate on the prompts, fulfillment messages, and LLM backend to improve the quality of the answers and the overall user experience.  Pay close attention to edge cases and how the LLM handles unexpected questions.
