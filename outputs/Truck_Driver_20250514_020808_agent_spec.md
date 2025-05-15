```json
{
  "agent": {
    "description": "A conversational AI agent designed to screen and interview candidates for a Truck Driver position. The agent aims to efficiently gather necessary information, assess candidate suitability, and answer common questions about the job and company. The tone is professional, friendly, and informative.",
    "name": "Truck Driver Recruitment Agent",
    "languageCode": "en"
  },
  "intent_truck_driver_recruitment": {
    "display_name": "Truck Driver Recruitment - Root",
    "description": "Root intent for the entire recruitment process.",
    "training_phrases": [
      "I am interested in the truck driver position",
      "I saw the job posting for truck drivers",
      "I want to apply for the truck driver job",
      "Are you hiring truck drivers?",
      "Tell me more about the truck driver opening"
    ],
    "parameters": [],
    "priority": 1,
    "isFallback": false
  },
  "intent_greeting": {
    "display_name": "Greeting",
    "description": "Greets the candidate at the beginning of the interview.",
    "training_phrases": [
      "Hello",
      "Hi",
      "Good morning",
      "Good afternoon",
      "Hey there"
    ],
    "parameters": [],
    "priority": 2,
    "isFallback": false,
    "response_messages": [
      {
        "text": {
          "text": [
            "Hello! Thanks for your interest in the Truck Driver position at [Company Name]. My name is [Agent Name], and I'll be conducting a preliminary interview. To begin, can you confirm that you have a valid Class A CDL?"
          ]
        }
      }
    ]
  },
  "intent_confirm_cdl": {
    "display_name": "Confirm CDL-A",
    "description": "Confirms that the candidate has a valid Class A Commercial Driver's License.",
    "training_phrases": [
      "Yes",
      "I do",
      "Yes, I have a Class A CDL",
      "I have a valid CDL-A",
       "affirmative"
    ],
    "parameters": [],
    "priority": 3,
    "isFallback": false
  },
  "intent_no_cdl": {
    "display_name": "No CDL-A",
    "description": "Handles the case where the candidate does not have a valid Class A Commercial Driver's License.",
    "training_phrases": [
      "No",
      "I don't",
      "I do not have a CDL-A",
      "I don't have a class A license",
       "negative"
    ],
    "parameters": [],
    "priority": 3,
    "isFallback": false,
    "response_messages": [
      {
        "text": {
          "text": [
            "Thank you for your interest.  A valid Class A CDL is a requirement for this position.  We appreciate your time.  Have a great day!"
          ]
        }
      }
    ]
  },
  "intent_get_otr_experience": {
    "display_name": "Get OTR Experience",
    "description": "Asks the candidate about their OTR experience.",
    "training_phrases": [
      "What is your OTR experience?",
      "How much OTR experience do you have?",
      "Tell me about your OTR driving experience",
      "Do you have any OTR experience?",
      "What's your over the road experience like?"
    ],
    "parameters": [],
    "priority": 4,
    "isFallback": false,
    "response_messages": [
      {
        "text": {
          "text": [
            "Great. Can you describe your OTR experience and the types of freight you've hauled?"
          ]
        }
      }
    ]
  },
  "intent_otr_experience_response": {
    "display_name": "OTR Experience Response",
    "description": "Captures the candidate's OTR experience.",
    "training_phrases": [
      "I have been driving OTR for 2 years.",
      "I've hauled dry van freight for 3 years.",
      "I have 5 years of experience hauling refrigerated goods OTR.",
      "I drove flatbed for 1 year and dry van for 2 years.",
      "Mostly general freight, about 4 years OTR."
    ],
    "parameters": [
      {
        "display_name": "otr_experience",
        "entity_type": "@sys.duration",
        "is_list": false,
        "required": false
      },
            {
        "display_name": "freight_type",
        "entity_type": "@freight_type",
        "is_list": true,
        "required": false
      }
    ],
    "priority": 5,
    "isFallback": false,
    "response_messages": [
      {
        "conditional_cases": [
          {
            "condition": "NOT $session.params.otr_experience OR NOT $session.params.freight_type",
            "case_content": [
              {
                "text": {
                  "text": [
                    "I understand you've had some experience. Now, regarding ELD usage, tell me about your experience with ELD devices and maintaining accurate logs."
                  ]
                }
              }
            ]
          },
          {
            "condition": "TRUE",
            "case_content": [
              {
                "text": {
                  "text": [
                    "Ok, you have $session.params.otr_experience. And you've been hauling $session.params.freight_type. Next, regarding ELD usage, tell me about your experience with ELD devices and maintaining accurate logs."
                  ]
                }
              }
            ]
          }
        ]
      }
    ]
  },
    "intent_get_eld_experience": {
    "display_name": "Get ELD Experience",
    "description": "Asks about candidate's experience with ELD devices and log maintenance.",
    "training_phrases": [
      "What's your ELD experience?",
      "Tell me about your ELD experience.",
      "Experience with ELD?",
      "Have you used ELDs?",
      "How experienced are you with electronic logging devices?"
    ],
    "parameters": [],
    "priority": 6,
    "isFallback": false,
    "response_messages": [
      {
        "text": {
          "text": [
            "Tell me about your experience with ELD devices and maintaining accurate logs."
          ]
        }
      }
    ]
  },
    "intent_eld_experience_response": {
    "display_name": "ELD Experience Response",
    "description": "Captures the candidate's experience with ELD devices and log maintenance.",
    "training_phrases": [
      "I have used ELDs for 5 years.",
      "I am very familiar with ELD.",
      "I have experience with Omnitracs and KeepTruckin.",
      "I used ELDs for log keeping at my last job.",
      "I'm not familiar with ELDs."
    ],
    "parameters": [
      {
        "display_name": "eld_experience",
        "entity_type": "@eld_type",
        "is_list": true,
        "required": false
      }
    ],
    "priority": 7,
    "isFallback": false,
        "response_messages": [
      {
        "text": {
          "text": [
            "Okay, thank you. Do you have any endorsements (Hazmat, Tanker, etc.)?"
          ]
        }
      }
    ]
  },
  "intent_get_endorsements": {
    "display_name": "Get Endorsements",
    "description": "Asks about candidate's endorsements.",
    "training_phrases": [
      "Any endorsements?",
      "Do you have endorsements?",
      "Tell me about your endorsements.",
      "Do you have hazmat or tanker endorsements?",
      "What endorsements do you have?"
    ],
    "parameters": [],
    "priority": 8,
    "isFallback": false,
    "response_messages": [
      {
        "text": {
          "text": [
            "Do you have any endorsements (Hazmat, Tanker, etc.)?"
          ]
        }
      }
    ]
  },
    "intent_endorsements_response": {
    "display_name": "Endorsements Response",
    "description": "Captures the candidate's endorsements.",
    "training_phrases": [
      "Yes, I have hazmat and tanker endorsements.",
      "I have a hazmat endorsement.",
      "I don't have any endorsements.",
      "I have a tanker endorsement.",
      "I have my doubles and triples endorsement."
    ],
    "parameters": [
      {
        "display_name": "endorsement_type",
        "entity_type": "@endorsement_type",
        "is_list": true,
        "required": false
      }
    ],
    "priority": 9,
    "isFallback": false,
            "response_messages": [
      {
        "text": {
          "text": [
            "Understood. Are you open to both refrigerated, dry van, and flatbed opportunities?"
          ]
        }
      }
    ]
  },
  "intent_freight_preference": {
    "display_name": "Freight Preference",
    "description": "Asks the candidate about their freight preferences.",
    "training_phrases": [
      "What is your freight preference?",
      "Do you have a preference for refrigerated or dry van?",
      "Are you open to different types of freight?",
      "Would you haul flatbed?",
      "Refrigerated, dry van, or flatbed?"
    ],
    "parameters": [],
    "priority": 10,
    "isFallback": false,
    "response_messages": [
      {
        "text": {
          "text": [
            "Are you open to both refrigerated, dry van, and flatbed opportunities?"
          ]
        }
      }
    ]
  },
  "intent_freight_preference_response": {
    "display_name": "Freight Preference Response",
    "description": "Captures the candidate's freight preferences.",
    "training_phrases": [
      "I prefer dry van.",
      "I'm open to anything.",
      "I only want to haul refrigerated.",
      "I prefer flatbed but I'm open to dry van.",
      "I'll haul anything."
    ],
    "parameters": [
      {
        "display_name": "freight_type",
        "entity_type": "@freight_type",
        "is_list": true,
        "required": false
      }
    ],
    "priority": 11,
    "isFallback": false,
                "response_messages": [
      {
        "text": {
          "text": [
            "Okay. Are you comfortable being out on the road for 2-3 weeks at a time?"
          ]
        }
      }
    ]
  },
    "intent_comfort_road_time": {
    "display_name": "Comfort Road Time",
    "description": "Asks if the candidate is comfortable with 2-3 weeks on the road.",
    "training_phrases": [
      "How do you feel about 2-3 weeks on the road?",
      "Are you okay with being out that long?",
      "Can you stay out for 2-3 weeks?",
      "Road Time?",
      "Weeks on the Road"
    ],
    "parameters": [],
    "priority": 12,
    "isFallback": false,
    "response_messages": [
      {
        "text": {
          "text": [
            "Are you comfortable being out on the road for 2-3 weeks at a time?"
          ]
        }
      }
    ]
  },
    "intent_comfort_road_time_response": {
    "display_name": "Comfort Road Time Response",
    "description": "Captures comfort level with being on the road for extended periods.",
    "training_phrases": [
      "Yes, I'm fine with that.",
      "2-3 weeks is fine.",
      "That's no problem for me.",
      "I'd prefer shorter trips.",
      "That's too long."
    ],
    "parameters": [
      {
        "display_name": "comfort_level",
        "entity_type": "@comfort_level",
        "is_list": false,
        "required": false
      }
    ],
    "priority": 13,
    "isFallback": false,
               "response_messages": [
      {
        "text": {
          "text": [
            "Got it. Do you have a rider or a pet that you would like to bring along, and are you familiar with our rider/pet policy?"
          ]
        }
      }
    ]
  },
  "intent_rider_pet_policy": {
    "display_name": "Rider/Pet Policy",
    "description": "Asks about rider/pet policy.",
    "training_phrases": [
      "Rider?",
      "Do you have a rider?",
      "Do you have any riders/pets?",
      "Pet?",
      "Do you want to bring a pet"
    ],
    "parameters": [],
    "priority": 14,
    "isFallback": false,
    "response_messages": [
      {
        "text": {
          "text": [
            "Do you have a rider or a pet that you would like to bring along, and are you familiar with our rider/pet policy?"
          ]
        }
      }
    ]
  },
  "intent_rider_pet_response": {
    "display_name": "Rider/Pet Response",
    "description": "Captures information regarding rider/pet policy.",
    "training_phrases": [
      "Yes, I have a dog.",
      "I want to bring my wife along.",
      "No, I don't have any riders or pets.",
      "I'm familiar with the pet policy.",
      "I have a cat that goes with me."
    ],
    "parameters": [
      {
        "display_name": "rider_pet",
        "entity_type": "@rider_pet",
        "is_list": false,
        "required": false
      }
    ],
    "priority": 15,
    "isFallback": false,
                   "response_messages": [
      {
        "text": {
          "text": [
            "Okay. Tell me about your safety record and any incidents you've had in the past."
          ]
        }
      }
    ]
  },
    "intent_safety_record": {
    "display_name": "Safety Record",
    "description": "Asks about the candidate's safety record.",
    "training_phrases": [
      "Safety?",
      "Tell me about your safety record.",
      "Past incidents?",
      "What is your safety record like?",
      "Incidents in the past?"
    ],
    "parameters": [],
    "priority": 16,
    "isFallback": false,
    "response_messages": [
      {
        "text": {
          "text": [
            "Tell me about your safety record and any incidents you've had in the past."
          ]
        }
      }
    ]
  },
    "intent_safety_record_response": {
    "display_name": "Safety Record Response",
    "description": "Captures information regarding the safety record.",
    "training_phrases": [
      "I have a clean driving record.",
      "I had one accident 3 years ago.",
      "No accidents in 5 years.",
      "I have a great safety record.",
      "I have no violations."
    ],
    "parameters": [
      {
        "display_name": "safety_record",
        "entity_type": "@safety_record",
        "is_list": false,
        "required": false
      },
      {
        "display_name": "accident_details",
        "entity_type": "@sys.any",
        "is_list": false,
        "required": false
      }
    ],
    "priority": 17,
    "isFallback": false,
                   "response_messages": [
      {
        "text": {
          "text": [
            "Thank you for that information. That concludes the preliminary interview. A recruiter will be in touch with you soon to discuss your application further. Do you have any questions for me before we end the conversation?"
          ]
        }
      }
    ]
  },
  "intent_candidate_questions": {
    "display_name": "Candidate Questions",
    "description": "Handles general questions from the candidate at the end of the preliminary interview.",
    "training_phrases": [
      "What kind of trucks do you have?",
      "What is your idle policy?",
      "How are the dispatchers?",
      "What kind of benefits do you offer besides health insurance?",
      "What is the average length of haul?",
      "What is the process for getting home time approved?",
       "I have a question",
       "Any other information?",
       "I would like to ask some questions."
    ],
    "parameters": [],
    "priority": 18,
    "isFallback": false
  },
  "intent_negative_response": {
    "display_name": "Negative Response",
    "description": "Handles negative responses or refusals to answer.",
    "training_phrases": [
      "I don't want to answer that",
      "I'd rather not say",
      "No",
      "I don't know",
      "That's confidential"
    ],
    "parameters": [],
    "priority": 19,
    "isFallback": true,
    "response_messages": [
      {
        "text": {
          "text": [
            "Understood. Thank you for your time."
          ]
        }
      }
    ]
  },
  "entity_type_freight_type": {
    "display_name": "freight_type",
    "kind": "KIND_MAP",
    "entities": [
      {
        "value": "dry van",
        "synonyms": [
          "dry van",
          "general freight",
          "box freight"
        ]
      },
      {
        "value": "refrigerated",
        "synonyms": [
          "refrigerated",
          "reefer",
          "temperature-controlled",
          "produce"
        ]
      },
      {
        "value": "flatbed",
        "synonyms": [
          "flatbed",
          "open deck",
          "construction materials",
          "steel"
        ]
      },
      {
        "value": "tanker",
        "synonyms": [
          "tanker",
          "liquid freight",
          "chemical freight",
          "gasoline"
        ]
      },
      {
        "value": "hazmat",
        "synonyms": [
          "hazmat",
          "hazardous materials",
          "dangerous goods"
        ]
      }
    ]
  },
  "entity_type_endorsement_type": {
    "display_name": "endorsement_type",
    "kind": "KIND_MAP",
    "entities": [
      {
        "value": "Hazmat",
        "synonyms": [
          "Hazmat",
          "H",
          "Hazardous Materials"
        ]
      },
      {
        "value": "Tanker",
        "synonyms": [
          "Tanker",
          "N",
          "Tank Vehicle"
        ]
      },
      {
        "value": "Doubles/Triples",
        "synonyms": [
          "Doubles/Triples",
          "T"
        ]
      },
      {
        "value": "Passenger",
        "synonyms": [
          "Passenger",
          "P"
        ]
      },
      {
        "value": "School Bus",
        "synonyms": [
          "School Bus",
          "S"
        ]
      }
    ]
  },
  "entity_type_comfort_level": {
    "display_name": "comfort_level",
    "kind": "KIND_MAP",
    "entities": [
      {
        "value": "comfortable",
        "synonyms": [
          "comfortable",
          "okay",
          "fine",
          "no problem",
          "I'm okay with that",
          "yes",
          "agree",
          "affirmative"
        ]
      },
      {
        "value": "uncomfortable",
        "synonyms": [
          "uncomfortable",
          "not okay",
          "that's too long",
          "I'd prefer shorter trips",
          "no",
          "disagree",
          "negative"
        ]
      }
    ]
  },
   "entity_type_rider_pet": {
    "display_name": "rider_pet",
    "kind": "KIND_MAP",
    "entities": [
      {
        "value": "rider",
        "synonyms": [
          "I have a rider.",
          "rider",
          "wife",
          "husband",
          "child",
          "friend"
        ]
      },
      {
        "value": "pet",
        "synonyms": [
          "pet",
          "dog",
          "cat",
          "hamster",
          "goldfish"
        ]
      },
            {
        "value": "no",
        "synonyms": [
          "no",
          "nope",
          "none",
          "I don't",
          "I do not"
        ]
      }
    ]
  },
  "entity_type_safety_record": {
    "display_name": "safety_record",
    "kind": "KIND_MAP",
    "entities": [
      {
        "value": "clean",
        "synonyms": [
          "clean",
          "good",
          "excellent",
          "no accidents",
          "safe"
        ]
      },
      {
        "value": "accidents",
        "synonyms": [
          "accident",
          "incidents",
          "violations"
        ]
      }
    ]
  },
  "entity_type_eld_type": {
    "display_name": "eld_type",
    "kind": "KIND_MAP",
    "entities": [
      {
        "value": "Omnitracs",
        "synonyms": [
          "Omnitracs",
          "Qualcomm",
          "Omnitracs ELD"
        ]
      },
      {
        "value": "Peoplenet",
        "synonyms": [
          "Peoplenet",
          "TMW Systems",
          "Peoplenet ELD"
        ]
      },
      {
        "value": "KeepTruckin",
        "synonyms": [
          "KeepTruckin",
          "KeepTruckin ELD",
          "Keeptrucking"
        ]
      },
            {
        "value": "Samsara",
        "synonyms": [
          "Samsara",
          "Samsara ELD"
        ]
      },
           {
        "value": "Transflo",
        "synonyms": [
          "Transflo",
          "Transflo ELD"
        ]
      }
    ]
  },
  "route_truck_driver_recruitment_root": {
    "description": "Root for the Truck Driver Recruitment",
    "intent": "Truck Driver Recruitment - Root",
    "targetPage": "Truck Driver Recruitment Start"
  },
  "route_greeting": {
    "description": "Route the greeting intent to the truck driver recruitment interview flow.",
    "intent": "Greeting",
    "targetPage": "Truck Driver Recruitment Start"
  },
  "route_confirm_cdl": {
    "description": "Routes confirmed CDL-A to the next question.",
    "intent": "Confirm CDL-A",
    "targetPage": "Get OTR Experience"
  },
    "route_no_cdl": {
    "description": "Routes user without CDL-A to end of interview.",
    "intent": "No CDL-A",
    "targetPage": "END_SESSION"
  },
    "route_otr_exp": {
    "description": "Routes OTR Experience question to the next question.",
    "intent": "Get OTR Experience",
    "targetPage": "OTR Experience Response"
  },
  "route_otr_exp_response": {
    "description": "Routes OTR Experience response to the next question",
    "intent": "OTR Experience Response",
    "targetPage": "Get ELD Experience"
  },
    "route_eld_exp": {
    "description": "Routes ELD Experience question to the next question.",
    "intent": "Get ELD Experience",
    "targetPage": "ELD Experience Response"
  },
  "route_eld_exp_response": {
    "description": "Routes ELD Experience response to the next question",
    "intent": "ELD Experience Response",
    "targetPage": "Get Endorsements"
  },
  "route_endorsements": {
    "description": "Routes endorsements question to endorsements response.",
    "intent": "Get Endorsements",
    "targetPage": "Endorsements Response"
  },
    "route_endorsements_response": {
    "description": "Routes endorsements response to freight preference.",
    "intent": "Endorsements Response",
    "targetPage": "Freight Preference"
  },
  "route_freight_pref": {
    "description": "Routes the freight preference question to freight preference response.",
    "intent": "Freight Preference",
    "targetPage": "Freight Preference Response"
  },
   "route_freight_pref_response": {
    "description": "Routes freight preference response to comfort road time question.",
    "intent": "Freight Preference Response",
    "targetPage": "Comfort Road Time"
  },
    "route_road_time": {
    "description": "Routes comfort with road time question to road time response",
    "intent": "Comfort Road Time",
    "targetPage": "Comfort Road Time Response"
  },
    "route_road_time_response": {
    "description": "Routes road time response to rider/pet policy",
    "intent": "Comfort Road Time Response",
    "targetPage": "Rider/Pet Policy"
  },
   "route_rider_pet_policy": {
    "description": "Routes rider/pet question to rider/pet policy response",
    "intent": "Rider/Pet Policy",
    "targetPage": "Rider/Pet Response"
  },
  "route_rider_pet_response": {
    "description": "Routes rider/pet response to safety record question",
    "intent": "Rider/Pet Response",
    "targetPage": "Safety Record"
  },
   "route_safety_record": {
    "description": "Routes safety record question to safety record response",
    "intent": "Safety Record",
    "targetPage": "Safety Record Response"
  },
    "route_safety_record_response": {
    "description": "Routes safety record response to candidate questions",
    "intent": "Safety Record Response",
    "targetPage": "Candidate Questions"
  },
  "route_candidate_questions": {
    "description": "Routes the candidate question intent to the pre-defined responses based on the question asked.",
    "intent": "Candidate Questions",
     "condition": "$intent = \"What kind of trucks do you have?\"",
     "targetPage": "trucks_do_you_have"
  },
    "route_candidate_questions_2": {
    "description": "Routes the candidate question intent to the pre-defined responses based on the question asked.",
    "intent": "Candidate Questions",
     "condition": "$intent = \"What is your idle policy?\"",
     "targetPage": "idle_policy"
  },
     "route_candidate_questions_3": {
    "description": "Routes the candidate question intent to the pre-defined responses based on the question asked.",
    "intent": "Candidate Questions",
     "condition": "$intent = \"How are the dispatchers?\"",
     "targetPage": "dispatchers"
  },
    "route_candidate_questions_4": {
    "description": "Routes the candidate question intent to the pre-defined responses based on the question asked.",
    "intent": "Candidate Questions",
     "condition": "$intent = \"What kind of benefits do you offer besides health insurance?\"",
     "targetPage": "other_benefits"
  },
    "route_candidate_questions_5": {
    "description": "Routes the candidate question intent to the pre-defined responses based on the question asked.",
    "intent": "Candidate Questions",
     "condition": "$intent = \"What is the average length of haul?\"",
     "targetPage": "average_haul"
  },
    "route_candidate_questions_6": {
    "description": "Routes the candidate question intent to the pre-defined responses based on the question asked.",
    "intent": "Candidate Questions",
     "condition": "$intent = \"What is the process for getting home time approved?\"",
     "targetPage": "home_time_process"
  },
      "route_candidate_questions_other": {
    "description": "Routes unhandled candidate questions to the end of session",
    "intent": "Candidate Questions",
     "targetPage": "END_SESSION"
  },
  "route_negative_response": {
    "description": "Routes the fallback intent (negative responses) to end of session.",
    "intent": "Negative Response",
    "targetPage": "END_SESSION"
  },
  "page_truck_driver_recruitment_start": {
    "display_name": "Truck Driver Recruitment Start",
    "entry_fulfillment": {
      "messages": [
        {
          "text": {
            "text": [
              "Can you confirm that you have a valid Class A CDL?"
            ]
          }
        }
      ]
    }
  },
  "page_otr_experience": {
    "display_name": "Get OTR Experience",
    "entry_fulfillment": {
      "messages": [
        {
          "text": {
            "text": [
              "Great. Can you describe your OTR experience and the types of freight you've hauled?"
            ]
          }
        }
      ]
    }
  },
   "page_get_eld_experience": {
    "display_name": "Get ELD Experience",
    "entry_fulfillment": {
      "messages": [
        {
          "text": {
            "text": [
              "Next, regarding ELD usage, tell me about your experience with ELD devices and maintaining accurate logs."
            ]
          }
        }
      ]
    }
  },
    "page_get_endorsements": {
    "display_name": "Get Endorsements",
    "entry_fulfillment": {
      "messages": [
        {
          "text": {
            "text": [
              "Do you have any endorsements (Hazmat, Tanker, etc.)?"
            ]
          }
        }
      ]
    }
  },
    "page_freight_preference": {
    "display_name": "Freight Preference",
    "entry_fulfillment": {
      "messages": [
        {
          "text": {
            "text": [
              "Are you open to both refrigerated, dry van, and flatbed opportunities?"
            ]
          }
        }
      ]
    }
  },
  "page_comfort_road_time": {
    "display_name": "Comfort Road Time",
    "entry_fulfillment": {
      "messages": [
        {
          "text": {
            "text": [
              "Are you comfortable being out on the road for 2-3 weeks at a time?"
            ]
          }
        }
      ]
    }
  },
  "page_rider_pet_policy": {
    "display_name": "Rider/Pet Policy",
    "entry_fulfillment": {
      "messages": [
        {
          "text": {
            "text": [
              "Do you have a rider or a pet that you would like to bring along, and are you familiar with our rider/pet policy?"
            ]
          }
        }
      ]
    }
  },
  "page_safety_record": {
    "display_name": "Safety Record",
    "entry_fulfillment": {
      "messages": [
        {
          "text": {
            "text": [
              "Tell me about your safety record and any incidents you've had in the past."
            ]
          }
        }
      ]
    }
  },
  "page_candidate_questions": {
    "display_name": "Candidate Questions",
    "entry_fulfillment": {
      "messages": [
        {
          "text": {
            "text": [
              "Thank you for that information. That concludes the preliminary interview. A recruiter will be in touch with you soon to discuss your application further. Do you have any questions for me before we end the conversation?"
            ]
          }
        }
      ]
    }
  },
  "page_trucks_do_you_have": {
    "display_name": "trucks_do_you_have",
    "entry_fulfillment": {
      "messages": [
        {
          "text": {
            "text": [
              "We have a fleet of newer model trucks, primarily Freightliner Cascadias and Kenworth T680s, equipped with automatic transmissions and the latest safety technology."
            ]
          }
        },
                {
          "text": {
            "text":