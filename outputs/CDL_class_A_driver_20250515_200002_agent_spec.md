```json
{
  "agent": {
    "name": "FEDx CDL Driver Recruiter",
    "description": "A Dialogflow CX agent for recruiting CDL Class A drivers for FEDx.",
    "defaultLanguageCode": "en",
    "timeZone": "America/Chicago"
  },
  "entityTypes": [
    {
      "name": "@yes_no",
      "kind": "KIND_MAP",
      "entities": [
        {
          "value": "yes",
          "synonyms": [
            "yes",
            "yeah",
            "yep",
            "okay",
            "sure",
            "absolutely",
            "definitely"
          ]
        },
        {
          "value": "no",
          "synonyms": [
            "no",
            "nope",
            "nah",
            "not really",
            "not interested",
            "not at this time"
          ]
        }
      ]
    }
  ],
  "flows": [
    {
      "name": "Main Flow",
      "startPage": "Start",
      "eventHandlers": [
        {
          "event": "sys.no-match-default",
          "triggerFulfillment": {
            "messages": [
              {
                "text": {
                  "text": [
                    "Sorry, I didn't understand that. Could you please rephrase?"
                  ]
                }
              }
            ]
          },
          "transitionRoutes": [
            {
              "targetPage": "$current",
              "condition": "true"
            }
          ]
        },
                {
          "event": "sys.no-input-default",
          "triggerFulfillment": {
            "messages": [
              {
                "text": {
                  "text": [
                    "Are you still there?  I didn't hear you.  Could you please respond?"
                  ]
                }
              }
            ]
          },
          "transitionRoutes": [
            {
              "targetPage": "$current",
              "condition": "true"
            }
          ]
        }
      ],
      "pages": [
        {
          "name": "Start",
          "entryFulfillment": {
            "messages": [
              {
                "text": {
                  "text": [
                    "Hi, this is RecruitAI from FEDx. This call is regarding the CDL Class A driver position at FEDx you applied for. Is this a good time to talk about it?"
                  ]
                }
              }
            ],
            "setParameterActions": [
              {
                "parameter": "company_name",
                "value": "FEDx"
              },
              {
                "parameter": "position",
                "value": "CDL Class A driver"
              }
            ]
          },
          "form": {
            "parameters": [
              {
                "name": "good_time",
                "displayName": "good_time",
                "entityType": "@yes_no",
                "required": true,
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
                  },
                  "repromptEventHandlers": [
                    {
                      "event": "sys.no-match-default",
                      "triggerFulfillment": {
                        "messages": [
                          {
                            "text": {
                              "text": [
                                "I didn't understand.  Please answer yes or no."
                              ]
                            }
                          }
                        ]
                      }
                    },
                    {
                      "event": "sys.no-input-default",
                      "triggerFulfillment": {
                        "messages": [
                          {
                            "text": {
                              "text": [
                                "Are you still there? Please answer yes or no if now is a good time."
                              ]
                            }
                          }
                        ]
                      }
                    }
                  ]
                }
              }
            ]
          },
          "transitionRoutes": [
            {
              "condition": "$page.params.good_time.resolved == true AND $page.params.good_time.value == \"yes\"",
              "triggerFulfillment": {
                "messages": [
                  {
                    "text": {
                      "text": [
                        "Great!"
                      ]
                    }
                  }
                ]
              },
              "targetPage": "Interest Confirmation"
            },
            {
              "condition": "$page.params.good_time.resolved == true AND $page.params.good_time.value == \"no\"",
              "triggerFulfillment": {
                "messages": [
                  {
                    "text": {
                      "text": [
                        "Okay, no problem. I will call back another time. Thank you!"
                      ]
                    }
                  }
                ]
              }
            }
          ]
        },
        {
          "name": "Interest Confirmation",
          "entryFulfillment": {
            "messages": [
              {
                "text": {
                  "text": [
                    "Are you interested in the CDL Class A driver position at FEDx?"
                  ]
                }
              }
            ]
          },
          "form": {
            "parameters": [
              {
                "name": "is_interested",
                "displayName": "is_interested",
                "entityType": "@yes_no",
                "required": true,
                "fillBehavior": {
                  "initialPromptFulfillment": {
                    "messages": [
                      {
                        "text": {
                          "text": [
                            "Are you interested?"
                          ]
                        }
                      }
                    ]
                  },
                                    "repromptEventHandlers": [
                    {
                      "event": "sys.no-match-default",
                      "triggerFulfillment": {
                        "messages": [
                          {
                            "text": {
                              "text": [
                                "I didn't understand.  Please answer yes or no."
                              ]
                            }
                          }
                        ]
                      }
                    },
                    {
                      "event": "sys.no-input-default",
                      "triggerFulfillment": {
                        "messages": [
                          {
                            "text": {
                              "text": [
                                "Are you still there? Please answer yes or no."
                              ]
                            }
                          }
                        ]
                      }
                    }
                  ]
                }
              }
            ]
          },
          "transitionRoutes": [
            {
              "condition": "$page.params.is_interested.resolved == true AND $page.params.is_interested.value == \"yes\"",
              "triggerFulfillment": {
                "messages": [
                  {
                    "text": {
                      "text": [
                        "Excellent!"
                      ]
                    }
                  }
                ]
              },
              "targetPage": "Name Confirmation"
            },
            {
              "condition": "$page.params.is_interested.resolved == true AND $page.params.is_interested.value == \"no\"",
              "triggerFulfillment": {
                "messages": [
                  {
                    "text": {
                      "text": [
                        "Okay, thank you for your time.  We will remove your application from consideration."
                      ]
                    }
                  }
                ]
              }
            }
          ]
        },
        {
          "name": "Name Confirmation",
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
                "name": "candidate_name",
                "displayName": "candidate_name",
                "entityType": "@sys.person",
                "required": true,
                "fillBehavior": {
                  "initialPromptFulfillment": {
                    "messages": [
                      {
                        "text": {
                          "text": [
                            "What is your name?"
                          ]
                        }
                      }
                    ]
                  },
                                    "repromptEventHandlers": [
                    {
                      "event": "sys.no-match-default",
                      "triggerFulfillment": {
                        "messages": [
                          {
                            "text": {
                              "text": [
                                "I didn't understand. Could you please spell your name if necessary?"
                              ]
                            }
                          }
                        ]
                      }
                    },
                    {
                      "event": "sys.no-input-default",
                      "triggerFulfillment": {
                        "messages": [
                          {
                            "text": {
                              "text": [
                                "Are you still there?  Please tell me your name."
                              ]
                            }
                          }
                        ]
                      }
                    }
                  ]
                }
              }
            ]
          },
          "transitionRoutes": [
            {
              "condition": "$page.params.candidate_name.resolved == true",
              "triggerFulfillment": {
                "messages": [
                  {
                    "text": {
                      "text": [
                        "Thank you, {candidate_name}!"
                      ]
                    }
                  }
                ]
              },
              "targetPage": "Previous Experience Check"
            }
          ]
        },
        {
          "name": "Previous Experience Check",
          "entryFulfillment": {
            "messages": [
              {
                "text": {
                  "text": [
                    "Have you worked for FEDx before?"
                  ]
                }
              }
            ]
          },
          "form": {
            "parameters": [
              {
                "name": "worked_for_company",
                "displayName": "worked_for_company",
                "entityType": "@yes_no",
                "required": true,
                "fillBehavior": {
                  "initialPromptFulfillment": {
                    "messages": [
                      {
                        "text": {
                          "text": [
                            "Have you worked for us previously?"
                          ]
                        }
                      }
                    ]
                  },
                                    "repromptEventHandlers": [
                    {
                      "event": "sys.no-match-default",
                      "triggerFulfillment": {
                        "messages": [
                          {
                            "text": {
                              "text": [
                                "I didn't understand. Please answer yes or no."
                              ]
                            }
                          }
                        ]
                      }
                    },
                    {
                      "event": "sys.no-input-default",
                      "triggerFulfillment": {
                        "messages": [
                          {
                            "text": {
                              "text": [
                                "Are you still there? Please answer yes or no."
                              ]
                            }
                          }
                        ]
                      }
                    }
                  ]
                }
              }
            ]
          },
          "transitionRoutes": [
            {
              "condition": "$page.params.worked_for_company.resolved == true AND $page.params.worked_for_company.value == \"yes\"",
              "triggerFulfillment": {
                "messages": [
                  {
                    "text": {
                      "text": [
                        "Okay."
                      ]
                    }
                  }
                ]
              },
              "targetPage": "Position Check"
            },
            {
              "condition": "$page.params.worked_for_company.resolved == true AND $page.params.worked_for_company.value == \"no\"",
              "triggerFulfillment": {
                "messages": [
                  {
                    "text": {
                      "text": [
                        "Alright."
                      ]
                    }
                  }
                ]
              },
              "targetPage": "Qualification Check 1"
            }
          ]
        },
        {
          "name": "Position Check",
          "entryFulfillment": {
            "messages": [
              {
                "text": {
                  "text": [
                    "What position did you have at FEDx when you worked here previously?"
                  ]
                }
              }
            ]
          },
          "form": {
            "parameters": [
              {
                "name": "former_position",
                "displayName": "former_position",
                "entityType": "@sys.text",
                "required": true,
                "fillBehavior": {
                  "initialPromptFulfillment": {
                    "messages": [
                      {
                        "text": {
                          "text": [
                            "What did you do?"
                          ]
                        }
                      }
                    ]
                  },
                                    "repromptEventHandlers": [
                    {
                      "event": "sys.no-match-default",
                      "triggerFulfillment": {
                        "messages": [
                          {
                            "text": {
                              "text": [
                                "I didn't understand. Can you please be more specific?"
                              ]
                            }
                          }
                        ]
                      }
                    },
                    {
                      "event": "sys.no-input-default",
                      "triggerFulfillment": {
                        "messages": [
                          {
                            "text": {
                              "text": [
                                "Are you still there? Please tell me your previous position."
                              ]
                            }
                          }
                        ]
                      }
                    }
                  ]
                }
              }
            ]
          },
          "transitionRoutes": [
            {
              "condition": "$page.params.former_position.resolved == true",
              "triggerFulfillment": {
                "messages": [
                  {
                    "text": {
                      "text": [
                        "Okay, thank you."
                      ]
                    }
                  }
                ]
              },
              "targetPage": "Qualification Check 1"
            }
          ]
        },
        {
          "name": "Qualification Check 1",
          "entryFulfillment": {
            "messages": [
              {
                "text": {
                  "text": [
                    "Do you have at least one year of verifiable OTR (Over The Road) experience driving a Class A vehicle?"
                  ]
                }
              }
            ],
            "setParameterActions": [
              {
                "parameter": "qualification_1",
                "value": "at least one year of verifiable OTR experience driving a Class A vehicle"
              }
            ]
          },
          "form": {
            "parameters": [
              {
                "name": "has_qualification_1",
                "displayName": "has_qualification_1",
                "entityType": "@yes_no",
                "required": true,
                "fillBehavior": {
                  "initialPromptFulfillment": {
                    "messages": [
                      {
                        "text": {
                          "text": [
                            "Do you have this experience?"
                          ]
                        }
                      }
                    ]
                  },
                                    "repromptEventHandlers": [
                    {
                      "event": "sys.no-match-default",
                      "triggerFulfillment": {
                        "messages": [
                          {
                            "text": {
                              "text": [
                                "I didn't understand. Please answer yes or no."
                              ]
                            }
                          }
                        ]
                      }
                    },
                    {
                      "event": "sys.no-input-default",
                      "triggerFulfillment": {
                        "messages": [
                          {
                            "text": {
                              "text": [
                                "Are you still there? Please answer yes or no."
                              ]
                            }
                          }
                        ]
                      }
                    }
                  ]
                }
              }
            ]
          },
          "transitionRoutes": [
            {
              "condition": "$page.params.has_qualification_1.resolved == true AND $page.params.has_qualification_1.value == \"yes\"",
              "triggerFulfillment": {
                "messages": [
                  {
                    "text": {
                      "text": [
                        "Great!"
                      ]
                    }
                  }
                ]
              },
              "targetPage": "Qualification Check 2"
            },
            {
              "condition": "$page.params.has_qualification_1.resolved == true AND $page.params.has_qualification_1.value == \"no\"",
              "triggerFulfillment": {
                "messages": [
                  {
                    "text": {
                      "text": [
                        "Unfortunately, this position requires OTR experience. Thank you for your time."
                      ]
                    }
                  }
                ]
              }
            }
          ]
        },
        {
          "name": "Qualification Check 2",
          "entryFulfillment": {
            "messages": [
              {
                "text": {
                  "text": [
                    "Are you at least 23 years old?"
                  ]
                }
              }
            ],
            "setParameterActions": [
              {
                "parameter": "age_requirement",
                "value": "23"
              }
            ]
          },
          "form": {
            "parameters": [
              {
                "name": "meets_age_requirement",
                "displayName": "meets_age_requirement",
                "entityType": "@yes_no",
                "required": true,
                "fillBehavior": {
                  "initialPromptFulfillment": {
                    "messages": [
                      {
                        "text": {
                          "text": [
                            "Is your age at least 23?"
                          ]
                        }
                      }
                    ]
                  },
                                    "repromptEventHandlers": [
                    {
                      "event": "sys.no-match-default",
                      "triggerFulfillment": {
                        "messages": [
                          {
                            "text": {
                              "text": [
                                "I didn't understand. Please answer yes or no."
                              ]
                            }
                          }
                        ]
                      }
                    },
                    {
                      "event": "sys.no-input-default",
                      "triggerFulfillment": {
                        "messages": [
                          {
                            "text": {
                              "text": [
                                "Are you still there? Please answer yes or no."
                              ]
                            }
                          }
                        ]
                      }
                    }
                  ]
                }
              }
            ]
          },
          "transitionRoutes": [
            {
              "condition": "$page.params.meets_age_requirement.resolved == true AND $page.params.meets_age_requirement.value == \"yes\"",
              "triggerFulfillment": {
                "messages": [
                  {
                    "text": {
                      "text": [
                        "Thank you."
                      ]
                    }
                  }
                ]
              },
              "targetPage": "Transportation Check"
            },
            {
              "condition": "$page.params.meets_age_requirement.resolved == true AND $page.params.meets_age_requirement.value == \"no\"",
              "triggerFulfillment": {
                "messages": [
                  {
                    "text": {
                      "text": [
                        "Unfortunately, you must be at least 23 years old to be considered for this position. Thank you for your time."
                      ]
                    }
                  }
                ]
              }
            }
          ]
        },
        {
          "name": "Transportation Check",
          "entryFulfillment": {
            "messages": [
              {
                "text": {
                  "text": [
                    "Do you have reliable transportation to get to the job every day in the Midwest region, routes within a 500-mile radius of the Chicago terminal?"
                  ]
                }
              }
            ]
          },
          "form": {
            "parameters": [
              {
                "name": "has_transportation",
                "displayName": "has_transportation",
                "entityType": "@yes_no",
                "required": true,
                "fillBehavior": {
                  "initialPromptFulfillment": {
                    "messages": [
                      {
                        "text": {
                          "text": [
                            "Do you have reliable transportation?"
                          ]
                        }
                      }
                    ]
                  },
                                    "repromptEventHandlers": [
                    {
                      "event": "sys.no-match-default",
                      "triggerFulfillment": {
                        "messages": [
                          {
                            "text": {
                              "text": [
                                "I didn't understand. Please answer yes or no."
                              ]
                            }
                          }
                        ]
                      }
                    },
                    {
                      "event": "sys.no-input-default",
                      "triggerFulfillment": {
                        "messages": [
                          {
                            "text": {
                              "text": [
                                "Are you still there? Please answer yes or no."
                              ]
                            }
                          }
                        ]
                      }
                    }
                  ]
                }
              }
            ]
          },
          "transitionRoutes": [
            {
              "condition": "$page.params.has_transportation.resolved == true AND $page.params.has_transportation.value == \"yes\"",
              "triggerFulfillment": {
                "messages": [
                  {
                    "text": {
                      "text": [
                        "Okay."
                      ]
                    }
                  }
                ]
              },
              "targetPage": "Current Employment"
            },
            {
              "condition": "$page.params.has_transportation.resolved == true AND $page.params.has_transportation.value == \"no\"",
              "triggerFulfillment": {
                "messages": [
                  {
                    "text": {
                      "text": [
                        "Unfortunately, you must have reliable transportation. Thank you for your time."
                      ]
                    }
                  }
                ]
              }
            }
          ]
        },
        {
          "name": "Current Employment",
          "entryFulfillment": {
            "messages": [
              {
                "text": {
                  "text": [
                    "Where are you currently working, and why are you looking to make a change?"
                  ]
                }
              }
            ]
          },
          "form": {
            "parameters": [
              {
                "name": "current_employer",
                "displayName": "current_employer",
                "entityType": "@sys.organization",
                "required": true,
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
                  },
                                    "repromptEventHandlers": [
                    {
                      "event": "sys.no-match-default",
                      "triggerFulfillment": {
                        "messages": [
                          {
                            "text": {
                              "text": [
                                "I didn't understand. Could you please spell the company name if necessary?"
                              ]
                            }
                          }
                        ]
                      }
                    },
                    {
                      "event": "sys.no-input-default",
                      "triggerFulfillment": {
                        "messages": [
                          {
                            "text": {
                              "text": [
                                "Are you still there? Please tell me where you currently work."
                              ]
                            }
                          }
                        ]
                      }
                    }
                  ]
                }
              },
              {
                "name": "reason_for_change",
                "displayName": "reason_for_change",
                "entityType": "@sys.text",
                "required": true,
                "fillBehavior": {
                  "initialPromptFulfillment": {
                    "messages": [
                      {
                        "text": {
                          "text": [
                            "Why are you looking to make a change?"
                          ]
                        }
                      }
                    ]
                  },
                                    "repromptEventHandlers": [
                    {
                      "event": "sys.no-match-default",
                      "triggerFulfillment": {
                        "messages": [
                          {
                            "text": {
                              "text": [
                                "I didn't understand. Can you please explain your reason?"
                              ]
                            }
                          }
                        ]
                      }
                    },
                    {
                      "event": "sys.no-input-default",
                      "triggerFulfillment": {
                        "messages": [
                          {
                            "text": {
                              "text": [
                                "Are you still there? Please tell me why you're looking for a new job."
                              ]
                            }
                          }
                        ]
                      }
                    }
                  ]
                }
              }
            ]
          },
          "transitionRoutes": [
            {
              "condition": "$page.params.current_employer.resolved == true AND $page.params.reason_for_change.resolved == true",
              "triggerFulfillment": {
                "messages": [
                  {
                    "text": {
                      "text": [
                        "Thank you."
                      ]
                    }
                  }
                ]
              },
              "targetPage": "Background Check"
            }
          ]
        },
        {
          "name": "Background Check",
          "entryFulfillment": {
            "messages": [
              {
                "text": {
                  "text": [
                    "To proceed, are you able to pass a background verification check, including a clean MVR and drug screening?"
                  ]
                }
              }
            ]
          },
          "form": {
            "parameters": [
              {
                "name": "can_pass_checks",
                "displayName": "can_pass_checks",
                "entityType": "@yes_no",
                "required": true,
                "fillBehavior": {
                  "initialPromptFulfillment": {
                    "messages": [
                      {
                        "text": {
                          "text": [
                            "Can you pass a background check?"
                          ]
                        }
                      }
                    ]
                  },
                                    "repromptEventHandlers": [
                    {
                      "event": "sys.no-match-default",
                      "triggerFulfillment": {
                        "messages": [
                          {
                            "text": {
                              "text": [
                                "I didn't understand. Please answer yes or no."
                              ]
                            }
                          }
                        ]
                      }
                    },
                    {
                      "event": "sys.no-input-default",
                      "triggerFulfillment": {
                        "messages": [
                          {
                            "text": {
                              "text": [
                                "Are you still there? Please answer yes or no."
                              ]
                            }
                          }
                        ]
                      }
                    }
                  ]
                }
              }
            ]
          },
          "transitionRoutes": [
            {
              "condition": "$page.params.can_pass_checks.resolved == true AND $page.params.can_pass_checks.value == \"yes\"",
              "triggerFulfillment": {
                "messages": [
                  {
                    "text": {
                      "text": [
                        "Okay, great."
                      ]
                    }
                  }
                ]
              },
              "targetPage": "Conclusion"
            },
            {
              "condition": "$page.params.can_pass_checks.resolved == true AND $page.params.can_pass_checks.value == \"no\"",
              "triggerFulfillment": {
                "messages": [
                  {
                    "text": {
                      "text": [
                        "Unfortunately, passing these checks is a requirement for the position. Thank you for your time."
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
              "intent": "Candidate.Question.Fallback",
              "targetPage": "Handle Candidate Questions"
            },
            {
              "intent": "Default Negative Intent",
              "triggerFulfillment": {
                "messages": [
                  {
                    "text": {
                      "text": [
                        "Okay, thank you for your time. We will be in touch."
                      ]
                    }
                  }
                ]
              }
            },
            {
              "intent": "Default Positive Intent",
              "triggerFulfillment": {
                "messages": [
                  {
                    "text": {
                      "text": [
                        "Okay, thank you for your time. We will be in touch."
                      ]
                    }
                  }
                ]
              }
            }
          ]
        },
         {
          "name": "Handle Candidate Questions",
          "entryFulfillment": {
            "messages": [
              {
                "text": {
                  "text": [
                    "One moment while I check on that for you..."
                  ]
                }
              }
            ],
              "webhook": "LLM_QuestionAnswering",
              "setParameterActions": [
                  {
                      "parameter": "previous_page",
                      "value": "$session.params.current_page"
                  }
              ]
          },
          "transitionRoutes": [
              {
                  "condition": "$session.params.llm_response != null",
                  "triggerFulfillment": {
                      "messages": [
                          {
                              "text": {
                                  "text": [
                                      "$session.params.llm_response"
                                  ]
                              }
                          },
                          {
                              "text": {
                                  "text": [
                                      "Do you have any further questions?"
                                  ]
                              }
                          }
                      ],
                      "setParameterActions": [
                          {
                              "parameter": "llm_response",
                              "value": "null"
                          }
                      ]
                  },
                  "targetPage": "Candidate Question Followup"
              }
          ]
      },
      {
          "name": "Candidate Question Followup",
          "transitionRoutes": [
              {
                  "intent": "Candidate.Question.Fallback",
                  "targetPage": "Handle Candidate Questions"
              },
              {
                  "intent": "Default Negative Intent",
                  "triggerFulfillment": {
                      "messages": [
                          {
                              "text": {
                                  "text": [
                                      "Alright, resuming the application process..."
                                  ]
                              }
                          }
                      ]
                  },
                  "targetPage": "$session.params.previous_page"
              },
               {
                  "intent": "Default Positive Intent",
                  "triggerFulfillment": {
                      "messages": [
                          {
                              "text": {
                                  "text": [
                                      "Alright, resuming the application process..."
                                  ]
                              }
                          }
                      ]
                  },
                  "targetPage": "$session.params.previous_page"
              }
          ]
      }
      ]
    }
  ],
  "intents": [
    {
      "name": "Candidate.Question.Fallback",
      "trainingPhrases": [
        {
          "parts": [
            {
              "text": "what is the salary?"
            }
          ]
        },
        {
          "parts": [
            {
              "text": "What are the working hours?"
            }
          ]
        },
        {
          "parts": [
            {
              "text": "What benefits are offered?"
            }
          ]
        },
        {
          "parts": [
            {
              "text": "When would the position start?"
            }
          ]
        },
        {
          "parts": [
            {
              "text": "What is the interview process?"
            }
          ]
        },
        {
          "parts": [
            {
              "text": "what kind of freight will I be hauling?"
            }
          ]
        },
        {
          "parts": [
            {
              "text": "tell me about the start times and delivery schedules"
            }
          ]
        },
        {
          "parts": [
            {
              "text": "How often will I be home?"
            }
          ]
        },
        {
          "parts": [
            {
              "text": "What type of trucks are in the fleet?"
            }
          ]
        },
        {
          "parts": [
            {
              "text": "What is the company's safety record?"
            }
          ]
        },
        {
          "parts": [
            {
              "text": "What is the process for requesting time off?"
            }
          ]
        },
        {
          "parts": [
            {
              "text": "Are there opportunities for advancement within the company?"
            }
          ]
        },
        {
          "parts": [
            {
              "text": "average age of trucks?"
            }
          ]
        },
        {
          "parts": [
            {
              "text": "What kind of technology does the company use for dispatch and communication?"
            }
          ]
        },
        {
          "parts": [
            {
              "text": "company culture?"
            }
          ]
        },
        {
          "parts": [
            {
              "text": "I have a question"
            }
          ]
        },
        {
          "parts": [
            {
              "text": "What is the job about?"
            }
          ]
        },
        {
          "parts": [
            {
              "text": "Tell me more about the benefits."
            }
          ]
        },
        {
          "parts": [
            {
              "text": "But, how much is the pay?"
            }
          ]
        },
        {
          "parts": [
            {
              "text": "more details please"
            }
          ]
        },
        {
          "parts": [
            {
              "text": "Tell me a little more."
            }
          ]
        }
      ]
    },
    {
      "name": "Default Negative Intent",
      "trainingPhrases": [
        {
          "parts": [
            {
              "text": "no"
            }