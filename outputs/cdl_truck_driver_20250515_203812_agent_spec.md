```json
{
  "agent_name": "FedExCDLRecruiter",
  "description": "A Dialogflow CX agent for recruiting CDL truck drivers for FedEx.",
  "company_name": "FedEx",
  "position": "CDL Truck Driver",
  "pages": [
    {
      "name": "Start",
      "display_name": "Start",
      "entry_fulfillment": {
        "messages": [
          {
            "text": {
              "text": [
                "Hi, this is RecruitAI from FedEx. This call is regarding the CDL Truck Driver position at FedEx you applied for. Is this a good time to talk about it?"
              ]
            }
          }
        ]
      },
      "form": {
        "parameters": [
          {
            "id": "good_time",
            "display_name": "good_time",
            "entity_type": "@yes_no",
            "required": true,
            "fill_behavior": {
              "initial_prompt_fulfillment": {
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
      "transition_routes": [
        {
          "condition": "$page.params.status = \"VALID\" AND $page.params.good_time.resolved = \"yes\"",
          "target_page": "InterestConfirmation",
          "name": "GoodTime_Yes"
        },
        {
          "condition": "$page.params.status = \"VALID\" AND $page.params.good_time.resolved = \"no\"",
          "trigger_fulfillment": {
            "messages": [
              {
                "text": {
                  "text": [
                    "No problem, I understand. When would be a better time to call you back?"
                  ]
                }
              }
            ]
          },
          "target_page": "EndSession",
          "name": "GoodTime_No"
        }
      ]
    },
    {
      "name": "InterestConfirmation",
      "display_name": "InterestConfirmation",
      "entry_fulfillment": {
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
            "id": "is_interested",
            "display_name": "is_interested",
            "entity_type": "@yes_no",
            "required": true,
            "fill_behavior": {
              "initial_prompt_fulfillment": {
                "messages": [
                  {
                    "text": {
                      "text": [
                        "Are you interested?"
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
          "condition": "$page.params.status = \"VALID\" AND $page.params.is_interested.resolved = \"yes\"",
          "target_page": "NameConfirmation",
          "name": "Interested_Yes"
        },
        {
          "condition": "$page.params.status = \"VALID\" AND $page.params.is_interested.resolved = \"no\"",
          "trigger_fulfillment": {
            "messages": [
              {
                "text": {
                  "text": [
                    "Okay, thanks for your time. Have a great day!"
                  ]
                }
              }
            ]
          },
          "target_page": "EndSession",
          "name": "Interested_No"
        }
      ]
    },
    {
      "name": "NameConfirmation",
      "display_name": "NameConfirmation",
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
            "id": "candidate_name",
            "display_name": "candidate_name",
            "entity_type": "@sys.person",
            "required": true,
            "fill_behavior": {
              "initial_prompt_fulfillment": {
                "messages": [
                  {
                    "text": {
                      "text": [
                        "Please confirm your name."
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
          "condition": "$page.params.status = \"VALID\"",
          "target_page": "PreviousExperienceCheck",
          "name": "NameConfirmed"
        }
      ]
    },
    {
      "name": "PreviousExperienceCheck",
      "display_name": "PreviousExperienceCheck",
      "entry_fulfillment": {
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
            "id": "worked_for_company",
            "display_name": "worked_for_company",
            "entity_type": "@yes_no",
            "required": true,
            "fill_behavior": {
              "initial_prompt_fulfillment": {
                "messages": [
                  {
                    "text": {
                      "text": [
                        "Have you worked at FedEx?"
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
          "condition": "$page.params.status = \"VALID\" AND $page.params.worked_for_company.resolved = \"yes\"",
          "target_page": "PositionCheck",
          "name": "WorkedForCompany_Yes"
        },
        {
          "condition": "$page.params.status = \"VALID\" AND $page.params.worked_for_company.resolved = \"no\"",
          "target_page": "QualificationCheck1",
          "name": "WorkedForCompany_No"
        }
      ]
    },
    {
      "name": "QualificationCheck1",
      "display_name": "QualificationCheck1",
      "entry_fulfillment": {
        "messages": [
          {
            "text": {
              "text": [
                "Do you have the required experience for this position, which is a minimum of 1 year of verifiable OTR experience?"
              ]
            }
          }
        ]
      },
      "form": {
        "parameters": [
          {
            "id": "has_qualification_1",
            "display_name": "has_qualification_1",
            "entity_type": "@yes_no",
            "required": true,
            "fill_behavior": {
              "initial_prompt_fulfillment": {
                "messages": [
                  {
                    "text": {
                      "text": [
                        "Do you have the required experience?"
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
          "condition": "$page.params.status = \"VALID\" AND $page.params.has_qualification_1.resolved = \"yes\"",
          "target_page": "QualificationCheck2",
          "name": "HasQualification1_Yes"
        },
        {
          "condition": "$page.params.status = \"VALID\" AND $page.params.has_qualification_1.resolved = \"no\"",
          "trigger_fulfillment": {
            "messages": [
              {
                "text": {
                  "text": [
                    "Unfortunately, this position requires a minimum of one year of verifiable OTR experience. Thank you for your time."
                  ]
                }
              }
            ]
          },
          "target_page": "EndSession",
          "name": "HasQualification1_No"
        }
      ]
    },
    {
      "name": "QualificationCheck2",
      "display_name": "QualificationCheck2",
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
            "id": "meets_age_requirement",
            "display_name": "meets_age_requirement",
            "entity_type": "@yes_no",
            "required": true,
            "fill_behavior": {
              "initial_prompt_fulfillment": {
                "messages": [
                  {
                    "text": {
                      "text": [
                        "Are you at least 23 years old?"
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
          "condition": "$page.params.status = \"VALID\" AND $page.params.meets_age_requirement.resolved = \"yes\"",
          "target_page": "TransportationCheck",
          "name": "MeetsAgeRequirement_Yes"
        },
        {
          "condition": "$page.params.status = \"VALID\" AND $page.params.meets_age_requirement.resolved = \"no\"",
          "trigger_fulfillment": {
            "messages": [
              {
                "text": {
                  "text": [
                    "Unfortunately, you must be at least 23 years of age to be considered for this position. Thank you for your time."
                  ]
                }
              }
            ]
          },
          "target_page": "EndSession",
          "name": "MeetsAgeRequirement_No"
        }
      ]
    },
    {
      "name": "TransportationCheck",
      "display_name": "TransportationCheck",
      "entry_fulfillment": {
        "messages": [
          {
            "text": {
              "text": [
                "Do you have reliable transportation to get to the job every day, to the Chicago terminal?"
              ]
            }
          }
        ]
      },
      "form": {
        "parameters": [
          {
            "id": "has_transportation",
            "display_name": "has_transportation",
            "entity_type": "@yes_no",
            "required": true,
            "fill_behavior": {
              "initial_prompt_fulfillment": {
                "messages": [
                  {
                    "text": {
                      "text": [
                        "Do you have reliable transportation?"
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
          "condition": "$page.params.status = \"VALID\" AND $page.params.has_transportation.resolved = \"yes\"",
          "target_page": "CurrentEmployment",
          "name": "HasTransportation_Yes"
        },
        {
          "condition": "$page.params.status = \"VALID\" AND $page.params.has_transportation.resolved = \"no\"",
          "trigger_fulfillment": {
            "messages": [
              {
                "text": {
                  "text": [
                    "Okay. We need to ensure the candidate has reliable transportation for the role."
                  ]
                }
              }
            ]
          },
          "target_page": "CurrentEmployment",
          "name": "HasTransportation_No"
        }
      ]
    },
    {
      "name": "CurrentEmployment",
      "display_name": "CurrentEmployment",
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
            "id": "current_employer",
            "display_name": "current_employer",
            "entity_type": "@sys.any",
            "required": true,
            "fill_behavior": {
              "initial_prompt_fulfillment": {
                "messages": [
                  {
                    "text": {
                      "text": [
                        "Could you tell me where you are currently working?"
                      ]
                    }
                  }
                ]
              }
            }
          },
          {
            "id": "reason_for_change",
            "display_name": "reason_for_change",
            "entity_type": "@sys.any",
            "required": true,
            "fill_behavior": {
              "initial_prompt_fulfillment": {
                "messages": [
                  {
                    "text": {
                      "text": [
                        "And what's the primary reason you're looking for a change?"
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
          "condition": "$page.params.status = \"VALID\"",
          "target_page": "BackgroundCheck",
          "name": "EmploymentInfoProvided"
        }
      ]
    },
    {
      "name": "BackgroundCheck",
      "display_name": "BackgroundCheck",
      "entry_fulfillment": {
        "messages": [
          {
            "text": {
              "text": [
                "Will you be able to pass a background verification check, including a clean MVR, and no DUIs or reckless driving convictions?"
              ]
            }
          }
        ]
      },
      "form": {
        "parameters": [
          {
            "id": "can_pass_checks",
            "display_name": "can_pass_checks",
            "entity_type": "@yes_no",
            "required": true,
            "fill_behavior": {
              "initial_prompt_fulfillment": {
                "messages": [
                  {
                    "text": {
                      "text": [
                        "Will you pass the background checks?"
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
          "condition": "$page.params.status = \"VALID\" AND $page.params.can_pass_checks.resolved = \"yes\"",
          "target_page": "Conclusion",
          "name": "CanPassChecks_Yes"
        },
        {
          "condition": "$page.params.status = \"VALID\" AND $page.params.can_pass_checks.resolved = \"no\"",
          "trigger_fulfillment": {
            "messages": [
              {
                "text": {
                  "text": [
                    "Unfortunately, a clean background check is required for this position. Thank you for your time."
                  ]
                }
              }
            ]
          },
          "target_page": "EndSession",
          "name": "CanPassChecks_No"
        }
      ]
    },
    {
      "name": "Conclusion",
      "display_name": "Conclusion",
      "entry_fulfillment": {
        "messages": [
          {
            "text": {
              "text": [
                "Thank you for your time, [Candidate Name]. Based on our conversation, we'll be in touch regarding next steps. Do you have any questions for me?"
              ]
            }
          }
        ]
      },
      "transition_routes": [
        {
          "condition": "true",
          "target_page": "CandidateQuestionHandling",
          "name": "CandidateQuestions"
        }
      ]
    },
    {
      "name": "EndSession",
      "display_name": "End Session",
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
      "transition_routes": [],
      "end_session": true
    },
    {
      "name": "CandidateQuestionHandling",
      "display_name": "Candidate Question Handling",
      "transition_routes": [
        {
          "condition": "$intent = \"general.faq\"",
          "trigger_fulfillment": {
            "messages": [
              {
                "text": {
                  "text": [
                    "Let me look that up for you..."
                  ]
                }
              }
            ],
            "webhook": "LLMQuestionAnsweringWebhook",
            "return_partial_responses": false
          },
          "target_page": "Conclusion",
          "name": "CandidateFAQIntent"
        },
        {
          "condition": "$intent = \"faq.salary\"",
          "trigger_fulfillment": {
            "messages": [
              {
                "text": {
                  "text": [
                    "The pay rate is $0.58-$0.65 per mile based on experience. You can expect to average 2,500-3,000 miles per week. Weekly pay is done via direct deposit and we offer a sign-on bonus of $3,000 paid in installments, as well as safety bonuses up to $500 quarterly."
                  ]
                }
              }
            ]
          },
          "target_page": "Conclusion",
          "name": "SalaryIntent"
        },
        {
          "condition": "$intent = \"faq.benefits\"",
          "trigger_fulfillment": {
            "messages": [
              {
                "text": {
                  "text": [
                    "We offer medical, dental, and vision insurance after 60 days, 401(k) with a 3% company match after 90 days, paid vacation (1 week after the first year), paid holidays, referral bonuses, newer equipment, and consistent freight."
                  ]
                }
              }
            ]
          },
          "target_page": "Conclusion",
          "name": "BenefitsIntent"
        },
                {
          "condition": "$intent = \"faq.location\"",
          "trigger_fulfillment": {
            "messages": [
              {
                "text": {
                  "text": [
                    "The location for this position will be working in the Midwest region, within a 500-mile radius of the Chicago terminal"
                  ]
                }
              }
            ]
          },
          "target_page": "Conclusion",
          "name": "LocationIntent"
        },
        {
          "condition": "true",
          "trigger_fulfillment": {
            "messages": [
              {
                "text": {
                  "text": [
                    "I'm sorry, I don't have the answer to that question. Let me connect you with a recruiter that can help with that information"
                  ]
                }
              }
            ]
          },
          "target_page": "EndSession",
          "name": "OtherQuestions"
        }
      ],
      "event_handlers": [],
      "form": {}
    },
    {
      "name": "PositionCheck",
      "display_name": "PositionCheck",
      "entry_fulfillment": {
        "messages": [
          {
            "text": {
              "text": [
                "Great! Have you worked as a CDL Truck Driver while working for FedEx before?"
              ]
            }
          }
        ]
      },
      "form": {
        "parameters": [
          {
            "id": "worked_position_company",
            "display_name": "worked_position_company",
            "entity_type": "@yes_no",
            "required": true,
            "fill_behavior": {
              "initial_prompt_fulfillment": {
                "messages": [
                  {
                    "text": {
                      "text": [
                        "Have you worked as a CDL Truck Driver before?"
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
          "condition": "$page.params.status = \"VALID\" AND $page.params.worked_position_company.resolved = \"yes\"",
          "target_page": "TransportationCheck",
          "name": "WorkedPositionCompany_Yes"
        },
        {
          "condition": "$page.params.status = \"VALID\" AND $page.params.worked_position_company.resolved = \"no\"",
          "target_page": "TransportationCheck",
          "name": "WorkedPositionCompany_No"
        }
      ]
    }
  ],
  "entities": [
    {
      "name": "yes_no",
      "display_name": "yes_no",
      "kind": "KIND_MAP",
      "auto_expansion_mode": "AUTO_EXPANSION",
      "entities": [
        {
          "value": "yes",
          "synonyms": [
            "yes",
            "yep",
            "yeah",
            "sure",
            "absolutely",
            "affirmative",
            "okay",
            "ok"
          ]
        },
        {
          "value": "no",
          "synonyms": [
            "no",
            "nope",
            "nah",
            "not really",
            "negative"
          ]
        }
      ]
    }
  ],
  "intents": [
        {
      "name": "general.faq",
      "training_phrases": [
        "How many paid holidays are offered?",
        "Are pets allowed in the trucks?",
        "What does the job require?",
        "What is the company culture?",
        "Explain to me about the job location.",
        "How many vacation days would I have?",
        "What does this job require?",
        "what do you know about this job",
        "Tell me more about the benefits",
        "Explain to me the shift.",
        "What is the work schedule?",
        "what are the pay rates",
        "Explain to me the pay.",
        "Tell me about the payment options.",
        "Tell me about payment",
        "Could you explain the pay?"
      ]
    },
    {
      "name": "faq.salary",
      "training_phrases": [
        "What is the pay?",
        "How much will I make?",
        "What's the salary?",
        "How much is the salary?",
        "tell me more about pay",
        "Could you describe pay?"
      ]
    },
    {
      "name": "faq.benefits",
      "training_phrases": [
        "What are the benefits?",
        "What health benefits are offered?",
        "what healthcare benefits are offered?",
        "tell me more about benefits",
        "Could you describe the benefits?"
      ]
    },
        {
      "name": "faq.location",
      "training_phrases": [
        "What is the job location?",
        "Where will I be working?",
        "what region does this role cover",
        "Where is this job located?",
        "tell me more about the region",
        "Could you describe the region?"
      ]
    }
  ],
  "webhooks": [
    {
      "name": "LLMQuestionAnsweringWebhook",
      "display_name": "LLMQuestionAnsweringWebhook",
      "generic_service": {
        "uri": "YOUR_LLM_WEBHOOK_ENDPOINT",
        "http_method": "POST",
        "request_headers": {
          "Content-Type": "application/json"
        }
      },
      "timeout": "30.0s",
      "disabled": false
    }
  ],
    "LLM_context": {
     "position_title": "cdl truck driver",
  "company_name": "fedx",
  "required_experience": "Minimum 1 year of verifiable OTR experience",
  "required_skills": [
    "Safely operate a Class A tractor-trailer",
    "Complete pre-trip and post-trip inspections",
    "Load and unload freight",
    "Maintain accurate logs using ELD system",
    "Communicate effectively with dispatch and customers",
    "Follow DOT regulations and company safety policies"
  ],
  "required_qualifications": [
    "Valid Class A Commercial Driver's License",
    "Clean MVR with no more than 2 moving violations in the past 3 years",
    "No DUIs or reckless driving convictions",
    "Must be at least 23 years of age",
    "Must pass DOT physical and drug screen",
    "High school diploma or GED preferred"
  ],
  "pay_rate": "$0.58-$0.65 per mile based on experience; Average weekly miles: 2,500-3,000; Weekly pay with direct deposit; Sign-on bonus: $3,000 (paid in installments); Safety bonuses up to $500 quarterly",
  "schedule_type": "Regional routes with 2-3 nights home per week",
  "location": "Midwest region, within a 500-mile radius of the Chicago terminal",
  "benefits": [
    "Medical, dental, and vision insurance after 60 days",
    "401(k) with 3% company match after 90 days",
    "Paid vacation (1 week after first year)",
    "Paid holidays",
    "Referral bonuses: $1,500 per hired driver",
    "Newer equipment with latest safety features",
    "Consistent freight - no seasonal layoffs"
  ],
  "job_description": "Transporting various goods to customers within a 500-mile radius of our Chicago terminal; occasional touch freight required.",
  "screening_requirements": [
    "DOT physical",
    "Drug screen",
    "Clean MVR",
    "Background check implied by MVR and DUI/reckless driving check"
  ],
  "common_candidate_questions": [
    "What type of freight will I be hauling?",
    "What are the truck specifications (make, model, transmission)?",
    "How is the sign-on bonus paid out?",
    "What is the average downtime between loads?",
    "What is the company's safety record and safety culture like?",
    "What is the dispatch process like?",
    "What are the opportunities for advancement within the company?",
    "Can you describe a typical week?",
    "What ELD system do you use?",
    "Who do I contact if I have vehicle problems on the road?"
  ],
  "question_answers": {
    "What type of freight will I be hauling?": "You'll be hauling a variety of general freight within the Midwest region.",
    "What are the truck specifications (make, model, transmission)?": "Our fleet consists of newer model trucks, generally Freightliner or Kenworth, equipped with automatic transmissions and advanced safety features.",
    "How is the sign-on bonus paid out?": "The sign-on bonus is paid out in installments over the first [Number] months of employment.",
    "What is the average downtime between loads?": "We strive to minimize downtime. Our dispatch team works hard to keep you moving with minimal waiting time between loads.",
    "What is the company's safety record and safety culture like?": "Safety is our top priority. We have a strong safety record and a culture that emphasizes safe driving practices. We provide ongoing safety training and reward safe drivers with quarterly bonuses.",
    "What is the dispatch process like?": "Our dispatchers are experienced and work closely with drivers to ensure efficient routes and timely deliveries. You'll communicate with them via phone or the ELD system.",
    "What are the opportunities for advancement within the company?": "We offer opportunities for advancement into roles such as driver trainer, dispatcher, or management positions for dedicated and skilled drivers.",
    "Can you describe a typical week?": "You'll be running regional routes, typically out 5-6 days a week with 2-3 nights home. You'll be responsible for pre-trip and post-trip inspections, safely transporting freight, and maintaining accurate logs.",
    "What ELD system do you use?": "We use [ELD system name]",
    "Who do I contact if I have vehicle problems on the road?": "You should contact our 24/7 roadside assistance team, the number will be provided during orientation"
  },
  "objection_handling": {
    "Objection: The pay is slightly lower than another offer I have.": "Response: We offer a comprehensive benefits package, including excellent medical benefits, a strong 401(k) match, consistent freight, and newer equipment. Consider the overall value, not just the per-mile rate. Also, our safety bonuses and referral program can significantly increase your earnings.",
    "Objection: I prefer long-haul over regional.": "Response: Our regional routes allow for a better work-life balance with more time at home. While long-haul can offer higher mileage, the time away from home can be difficult. Consider the benefits of being home 2-3 nights a week.",
    "Objection: I'm concerned about touch freight.": "Response: The 'touch freight' is occasional. We try to minimize it. It might include unloading a few boxes at a delivery point. Much of our freight is drop and hook.",
    "Objection: Worried about making the mileage targets.": "Response: We provide ample opportunity to hit those numbers. Our dispatchers prioritize mileage and we have consistent freight and minimal downtime.",
    "Objection: Only 1 week of vacation after a year": "Response: This is a standard benefit for new drivers. The vacation time increases with tenure. We also offer paid holidays from the start."
  },
  "key_screening_questions": [
    "Tell me about your experience with ELD systems.",
    "Describe a time you had to deal with a difficult customer or situation on the road and how you resolved it.",
    "Have you ever had any accidents or incidents? If so, please describe them.",
    "Are you comfortable with occasional touch freight?",
    "Do you have any endorsements on your CDL?",
    "What is your understanding of DOT regulations regarding hours of service?",
    "Why are you looking for a new driving position?",
    "Are you able to pass a DOT physical and drug screen?"
  ],
  "age_requirement": "23",
  "qualification_checks": [
    "Valid Class A CDL",
    "DOT Medical Card",
    "MVR Check (no more than 2 moving violations in the past 3 years)",
    "Background Check (no DUIs or reckless driving convictions)",
    "Verifiable OTR Experience (minimum 1 year)"
  ]
}
}
```

**Explanation and Key Considerations:**

1.  **Conversation Flow:** The JSON meticulously implements the specified conversation flow, ensuring the agent follows the defined path.

2.  **Parameters and Entities:** Each page has parameters to capture the user's responses. The `yes_no` entity is defined, making the agent understand affirmative and negative replies.  `@sys.person` and `@sys.any` are used where appropriate.

3.  **Transitions:**  `transition_routes` manage the flow, directing the conversation based on the values of the captured parameters (especially `@yes_no` entity values).

4.  **Fulfillment Messages:**  Messages in `entry_fulfillment` sections guide the user and confirm information, providing a natural conversational experience.  The `[Candidate Name]` placeholder in the `Conclusion` page would ideally be filled dynamically with the confirmed name from the `NameConfirmation` page using the `$page.params.candidate_name.resolved` parameter.

5.  **Candidate Question Handling:** This is the most complex part:
    *   **CandidateQuestionHandling Page:**  This page is the target after the standard conversation ends.
    *   **Fallback Intent:**  The `transition_routes` of `CandidateQuestionHandling` uses conditions like `$intent = "general.faq"`. This *requires* that the associated intents are configured in your Dialogflow CX agent and correctly detect user questions.
    *   **Webhook Integration (LLMQuestionAnsweringWebhook):** The `trigger_fulfillment` for the `general.faq` intent includes a `webhook` field set to `LLMQuestionAnsweringWebhook`.
        *   `uri`: **CRITICAL: You *must* replace `YOUR_LLM_WEBHOOK_ENDPOINT` with the actual URL of your deployed LLM endpoint.**
        *   `http_method`:  `POST` is almost always correct for LLM interactions.
        *   `request_headers`: Sets the `Content-Type` to `application/json`.
        *   `timeout`:  Set to 30 seconds, which is a reasonable default, but you might need to increase it if your LLM responses are consistently slow.
    * **State Management (Implicit):** The conversation state is *implicitly* managed here. After the LLM answers the question via the webhook, the flow returns to the `Conclusion` page to ask if there are further questions.

6.  **LLM Context (Important):** The `LLM_context` section contains the information needed by the LLM to generate relevant and accurate responses. The webhook will need to package this data and send it with the user's question to the LLM.

7.  **Key Improvements:**
    *   **More Robust Intent Matching**: Added intents `general.faq`, `faq.salary`, `faq.benefits` and `faq.location` with training phrases to better match user queries and trigger the LLM webhook.
    *   **Clarified Error Handling**: Added the additional transition route for "OtherQuestions" with a message suggesting connecting the candidate to a recruiter. This is a better user experience than simply failing to answer.
    *   **PositionCheck** Added the option of reconfirming the candidate has previously worked as a driver for FedEx before.

**Webhook Implementation (LLMQuestionAnsweringWebhook - `YOUR_LLM_WEBHOOK_ENDPOINT`)**

The LLM webhook will need to:

1.  **Receive the Request:** The webhook will receive a POST request from Dialogflow CX. The request body contains a lot of information. The user's question will typically be in the `query` field (check the Dialogflow CX webhook documentation for the exact structure).

2.  **Extract the Question and Context:** Extract the user's question and the `LLM_context` from the request.

3.  **Format the Prompt:** Construct a prompt for the LLM that includes the context and the question. A good prompt engineering strategy is *crucial* for the quality of the LLM's responses.  Here's an example prompt structure:

    ```
    "You are a friendly and helpful recruiter for FedEx, specialized in CDL Truck Driver positions.  Use the following information to answer the candidate's question.  If the information isn't enough say "I am unsure of this question. Let me get a recruiter".

    Context:
