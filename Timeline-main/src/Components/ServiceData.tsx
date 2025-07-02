
const serviceData = [
  {
    title: "Counselling in Primary Care",
    description: "Provides up to 8 counselling sessions for adults over 18 years who are medical card holders and experiencing mild to moderate psychological and emotional difficulties such as depression, anxiety, panic reactions, relationship problems, loss issues, and stress.",
    otherContact: "Referral through your GP or local primary care team.",
    users: ["Male", "Female", "Others"],
    serviceType: "Mental Well-being Support",
    image: "Image/serviceLogo/Counselling_in_Primary_Care.png"
  },
  {
    title: "DVR",
    description: "Provides long term counselling to people of all ages that are living with or have lived with domestic abuse in Galway City and County. Sessions are provided one-to one, via phone or Zoom. This service is free of charge\nOffers a range of services and supports to female victims of Domestic Violence and Abuse.",
    phone: "091866740 or 0877737957",
    users: ["Female", "Others"],
    website: "https://www.domesticviolenceresponse.com/",
    serviceType: ["Mental Well-being Support", "Domestic Abuse Support"],
    image: "Image/serviceLogo/DVR.png"
  },

  {
    title: "Pieta House",
    description: "Pieta House provides free counselling to those with suicidal ideation, those engaging in self-harm, and those bereaved by suicide. Their therapy model focuses on identifying and building resources and protective factors for the client.",
    phone: "1800247247",
    address: "2nd Floor, Lismoyle House, Merchants Rd, Galway, H91 FX4T",
    website: "https://www.pieta.ie/",
    users: ["Male", "Female", "Others"],
    serviceType: "Mental Well-being Support",
    image: "Image/serviceLogo/Pieta_House.png"
  },

  {
    title: "Court Accompaniment",
    description: "Provides emotional support, both before, during and after the court proceedings. Support you as you face your abusive partner on the day, clarify legal terminology for you, help you to come to terms with the decision of the courts, identify safety measures for you and your children following the court hearing. This service is free of charge.",
    phone: "0877737957",
    users: ["Female", "Others"],
    serviceType: "Legal Services",
    website: "https://www.domesticviolenceresponse.com/",
    image: "Image/serviceLogo/Court_Accompaniment.png"
  },

  {
    title: "Aware",
    description: "Aware is a national organization that offers free support, education, and information services to individuals affected by anxiety, depression, bipolar disorder, and related mood conditions.",
    phone: "1800 80 48 48",
    website: "http://www.aware.ie/",
    users: ["Male", "Female", "Others"],
    serviceType: "Mental Well-being Support",
    image: "Image/serviceLogo/Aware.png"
  },

  {
    title: "Western Region Drug and Alcohol Task Force Family Support",
    description: "This programme offers personalized aid, information, and referrals for families dealing with substance use among loved ones.",
    phone: "087-1465956",
    email: "carol.burke@wrdatf.ie",
    website: "wrdatf.ie",
    users: ["Male", "Female", "Others"],
    serviceType: "Mental Well-being Support",
    image: "Image/serviceLogo/Western_Region_Drug_and_Alcohol_Task_Force_Family_Support.png"
  },

  {
    title: "Your Mental Health information line",
    description: "Phone service to provide information on mental health supports and services available from the HSE.",
    phone: "1800 111 888",
    users: ["Male", "Female", "Others"],
    serviceType: "Mental Well-being Support",
    image: "Image/serviceLogo/Your_Mental_Health_information_line.png"
  },

  {
    title: "Male Advice Line",
    description: "Offers confidential advice and support for male victims of domestic violence and abuse.",
    phone: "1800 816 588",
    website: "http://mensnetwork.ie/",
    users: ["Male"],
    serviceType: ["Mental Well-being Support", "Domestic Abuse Support"],
    image: "Image/serviceLogo/The_National_Male_Advice_Line.png"
  },

  {
    title: "Simon Community",
    description: "Provides support and advice for individuals experiencing or at risk of homelessness. At Galway Simon, the client is always at the heart of what they do.",
    phone: "091 381828",
    users: ["Male", "Female", "Others"],
    serviceType: "Housing",
    image: "Image/serviceLogo/Simon_Community.png"
  },

  {
    title: "COPE Galway Homeless Services",
    description: "Provides advice, support, and facilities for individuals who are homeless or rough sleeping in Galway City. The centre is also a great social space to meet other people and grab a coffee, tea, soup or sandwich.",
    phone: "091 778 750",
    email: "info@copegalway.ie",
    address: "Calbro House, Tuam Road, Galway H91 XR97",
    users: ["Male", "Female", "Others"],
    website: "https://www.copegalway.ie/",
    serviceType: "Housing",
    image: "Image/serviceLogo/COPE_Galway_Homeless_Services.png"
  },

  {
    title: "Family Law Court",
    description: "Family Law deals with legal options relating to family and domestic matters including separation, divorce, maintenance, arrangements for children, and domestic violence.",
    address: "Galway Court Office - Courthouse Square, Galway, Co. Galway. H91 CDT6,",
    phone: "091 511500",
    email: "galwayfamily@courts.ie",
    users: ["Male", "Female", "Others"],
    serviceType: "Legal Services",
    image: "Image/serviceLogo/Family_Law_Court.png"
  },

  {
    title: "Legal Aid",
    description: "Provides comprehensive legal assistance to those unable to afford private solicitors. Services include legal advice, court representation, and family mediation.",
    address: "Galway's Francis Street",
    phone: "091 561650",
    email: "galwaylawcentre@legalaidboard.ie",
    users: ["Male", "Female", "Others"],
    serviceType: "Legal Services",
    image: "Image/serviceLogo/Legal_Aid.png"
  },

  {
    title: "Garda Síochána",
    description: "Provides support for domestic and sexual abuse victims, offering immediate response, advice, and assistance. Victims can call 999 for emergencies or visit local stations for private consultations.",
    phone: "999",
    address: "local stations",
    website: "http://garda.ie/",
    users: ["Male", "Female", "Others"],
    serviceType: "Domestic Abuse Support",
    image: "Image/serviceLogo/Garda_Síochána.png"
  },

  {
    title: "TUSLA Family Services",
    description: "Offers support for families facing difficulties including direct work with children, parental support, advice, advocacy, interagency meetings, and support against domestic violence.",
    phoneNumber: "0861713384 (North Galway Family Services Tuam)",
    website: "http://www.tusla.ie/",
    users: ["Male", "Female", "Others"],
    serviceType: ["Domestic Abuse Support", "Family Services"],
    image: "Image/serviceLogo/TUSLA_Family_Services.png"
  },

  {
    title: "TUSLA Social Work",
    description: "Provides frontline child welfare and protection in Galway. Social workers ensure child safety, well-being, and provide family support, including counseling and domestic violence services.",
    phoneNumber: "0861713384 (North Galway Family Services Tuam)",
    website: "http://www.tusla.ie/",
    users: ["Male", "Female", "Others"],
    serviceType: ["Domestic Abuse Support", "Family Services"],
    image: "Image/serviceLogo/TUSLA_Social_Work.png"
  },

  {
    title: "Galway Traveller Movement",
    description: "Advocates for the rights and cultural heritage of the Traveller community, focusing on accommodation, education, work, health, and combatting racism.",
    phone: "091 765390",
    email: "info@gtmtrav.ie",
    website: "http://gtmtrav.ie/",
    address: "The Plaza, 1 Headford Rd, Galway, H91 KC6V",
    users: ["Male", "Female", "Others"],
    serviceType: ["Family Services", "Education and Employment"],
    image: "Image/serviceLogo/Galway_Traveller_Movement.png"
  },

  {
    title: "Money Advice",
    description: "Delivers expert financial advice and budgeting services to individuals and families, empowering them to navigate financial challenges and manage debts.",
    phone: "0818072000",
    website: "https://mabs.ie/about/find-a-mabs-office",
    users: ["Male", "Female", "Others"],
    serviceType: "Financial",
    image: "Image/serviceLogo/Money_Advice.png"
  },

  {
    title: "Social Welfare",
    description: "Renders social welfare assistance including unemployment aid and family allowances.",
    phone: "0818 405060",
    email: "galway@welfare.ie",
    website: "www.gov.ie/intreo",
    users: ["Male", "Female", "Others"],
    serviceType: "Financial",
    image: "Image/serviceLogo/Social_Welfare.png"
  },

  {
    title: "The National Childcare Scheme",
    description: "Offers childcare services and financial support to families to help balance work and family life.",
    phone: "091-752039",
    website: "https://www.ncs.gov.ie/en/",
    users: ["Male", "Female"],
    serviceType: "Financial",
    image: "Image/serviceLogo/The_National_Childcare_Scheme.png"
  },

  {
    title: "Community Welfare Service",
    description: "Delivers welfare assistance including emergency relief and medical assistance at the community level.",
    website: "CWSGalway@welfare.ie",
    phone: "0818 607080",
    users: ["Male", "Female", "Others"],
    serviceType: "Financial",
    image: "Image/serviceLogo/Community_Welfare_Service.png"
  },

  {
    title: "FORUM Connemara",
    description: "A non-profit serving the Connemara community with supports and services, uplifting local lives and addressing regional needs.",
    phone: "095 41116",
    users: ["Male", "Female", "Others"],
    serviceType: "Education and Employment",
    image: "Image/serviceLogo/FORUM_Connemara.png"
  },

  {
    title: "No 4 Youth Service",
    description: "Addresses challenges including mental health, homelessness risks, providing information, homeless prevention, counselling, and educational assistance.",
    phone: "091 568 483",
    email: "youthservice@no4.ie",
    website: "https://www.no4.ie/",
    users: ["Youth"],
    serviceType: "Education and Employment",
    image: "Image/serviceLogo/No_4_Youth_Service.png"
  },

  {
    title: "Youth Work Ireland Counselling",
    description: "Provides counselling to youth, equipping them with tools to address life's challenges and emotional dilemmas.",
    phone: "0860247763",
    email: "aisling.dermody@youthgalway.ie",
    users: ["Youth"],
    serviceType: "How to Support",
    image: "Image/serviceLogo/Youth_Work_Ireland_Counselling.png"
  },

  {
    title: "                                          ! LGBTI+ Galway",
    description: "Advocates for and supports the LGBTI+ community in Galway through community-driven efforts.",
    phone: "089 497 5162",
    email: "info@amachlgbt.com",
    website: "https://www.amachlgbt.com/",
    users: ["Others"],
    serviceType: "How to Support",
    image: "Image/serviceLogo/AMACH_LGBTI_Galway.png"
  },

  {
    title: "Western Region Drug and Alcohol Task Force Family Support",
    description: "Comprehensive support for families facing substance-related challenges, ensuring holistic care and early interventions.",
    phone: "087-1465956",
    email: "carol.burke@wrdatf.ie",
    website: "wrdatf.ie",
    users: ["Male", "Female", "Others"],
    serviceType: "How to Support",
    image: "Image/serviceLogo/Western_Region_Drug_and_Alcohol_Task_Force_Family_Support.png"
  },

  {
    title: "Solas Og",
    description: "Supports children affected by domestic abuse in Galway through tailored support, therapeutic play, and group programs.",
    phone: "091 394880 / 394876",
    email: "solasog@copegalway.ie",
    users: ["Male", "Female", "Youth"],
    serviceType: "How to Support",
    image: "Image/serviceLogo/Solas_Og.png"
  },

  {
    title: "Rainbows",
    description: "Assists children facing bereavement and parental separation through group sessions for shared grief experiences.",
    phone: "086 8102015",
    email: "ask@rainbowsireland.ie",
    users: ["Youth"],
    serviceType: "How to Support",
    image: "Image/serviceLogo/Rainbows.png"
  },

  {
    title: "Jigsaw",
    description: "A primary care youth mental health service provider in Ireland, Jigsaw offers mental health support for young people aged 12-25 and their families, providing both online and in-person services around the country.",
    phone: "091 549 252",
    email: "galway@jigsaw.ie",
    users: ["Male", "Female", "Others", "Youth"],
    serviceType: ["Mental Well-being Support", "How to Support"],
    image: "Image/serviceLogo/Jigsaw.png"
  },

  {
    title: "Parenting After Domestic Violence",
    description: "Training for parents post-abuse, focusing on child welfare, maternal control, and violence-free environments.",
    phone: "091 866740 / 087 7737957",
    website: "https://www.domesticviolenceresponse.com/",
    users: ["Youth", "Female", "Others"],
    serviceType: "Parenting",
    image: "Image/serviceLogo/Parenting_After_Domestic_Violence.png"
  },

  {
    title: "Clann Resource Centre",
    description: "Offers counselling services including Play Therapy, Youth and Adolescent Counselling, and Adult Counselling on a sliding scale basis. Also provides social and educational classes, and supports referrals to other frontline services.",
    website: "clannrescentre.com",
    email: "3clanninfo@gmail.com",
    phone: "091 557633",
    users: ["Youth", "Female", "Others", "Male"],
    serviceType: "Parenting",
    image: "Image/serviceLogo/Clann_Resource_Centre.png"
  },

  {
    title: "Parenting Positively",
    description: "Free booklets for parents on issues affecting children and teenagers.",
    website: "https://shop.barnardos.ie/collections/parenting-positively",
    users: ["Male", "Female", "Others"],
    serviceType: "Parenting",
    image: "Image/serviceLogo/Parenting_Positively.png"
  },

  {
    title: "Parents Plus",
    description: "Practical parenting and mental health courses designed for professionals working with families. Courses focus on different age groups.",
    otherContact: "Contact your local Family Support Service,",
    website: "https://www.parentsplus.ie/",
    users: ["Youth"],
    serviceType: "Parenting",
    image: "Image/serviceLogo/Parents_Plus.png"
  }
]



export default serviceData;

