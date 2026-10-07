import random

quiz_data = {

"Data Scientist": [
{"q":"What is data preprocessing?","opt":["Cleaning data","Deleting data","Ignoring data"],"ans":"Cleaning data"},
{"q":"Which library is used for analysis?","opt":["NumPy","Pandas","TensorFlow"],"ans":"Pandas"},
{"q":"What is overfitting?","opt":["Simple model","Complex model","No training"],"ans":"Complex model"},
{"q":"Supervised learning uses?","opt":["Labeled data","Unlabeled","No data"],"ans":"Labeled data"},
{"q":"Classification algorithm?","opt":["Linear Regression","Logistic Regression","Clustering"],"ans":"Logistic Regression"},
{"q":"Feature means?","opt":["Column","Row","Table"],"ans":"Column"},
{"q":"Dataset is?","opt":["Data collection","Single value","Graph"],"ans":"Data collection"},
{"q":"ML stands for?","opt":["Machine Learning","Manual Learning","None"],"ans":"Machine Learning"}
],

"Web Developer": [
{"q":"HTML stands for?","opt":["Hyper Text Markup Language","High Text Machine Language","None"],"ans":"Hyper Text Markup Language"},
{"q":"CSS is used for?","opt":["Structure","Styling","Database"],"ans":"Styling"},
{"q":"JavaScript is used for?","opt":["Logic","Design","Database"],"ans":"Logic"},
{"q":"Responsive means?","opt":["Mobile friendly","Slow","Static"],"ans":"Mobile friendly"},
{"q":"Bootstrap is?","opt":["Framework","Language","Database"],"ans":"Framework"},
{"q":"React is?","opt":["Library","Database","Tool"],"ans":"Library"},
{"q":"ID vs Class?","opt":["Same","ID unique","Class unique"],"ans":"ID unique"},
{"q":"API is?","opt":["Interface","Database","Server"],"ans":"Interface"}
],

"AI Engineer": [
{"q":"AI stands for?","opt":["Artificial Intelligence","Auto Input","None"],"ans":"Artificial Intelligence"},
{"q":"Neural network is?","opt":["Brain model","Database","UI"],"ans":"Brain model"},
{"q":"Deep learning is?","opt":["Subset of ML","Database","UI"],"ans":"Subset of ML"},
{"q":"TensorFlow is?","opt":["Library","Language","Tool"],"ans":"Library"},
{"q":"NLP is?","opt":["Language processing","Database","UI"],"ans":"Language processing"},
{"q":"Model training means?","opt":["Learning","Deleting","Ignoring"],"ans":"Learning"},
{"q":"Dataset is?","opt":["Data collection","Single value","None"],"ans":"Data collection"},
{"q":"Prediction means?","opt":["Future guess","Delete","Ignore"],"ans":"Future guess"}
],

"Cybersecurity Analyst": [
{"q":"Firewall is?","opt":["Security system","Database","UI"],"ans":"Security system"},
{"q":"Phishing is?","opt":["Attack","Game","Tool"],"ans":"Attack"},
{"q":"Encryption means?","opt":["Secure data","Delete data","Ignore"],"ans":"Secure data"},
{"q":"Penetration testing?","opt":["Testing security","Coding","Design"],"ans":"Testing security"},
{"q":"Malware is?","opt":["Virus","App","Tool"],"ans":"Virus"},
{"q":"VPN is?","opt":["Secure network","Database","UI"],"ans":"Secure network"},
{"q":"Linux used for?","opt":["Security","Design","Gaming"],"ans":"Security"},
{"q":"Ethical hacking is?","opt":["Legal hacking","Illegal","None"],"ans":"Legal hacking"}
],

"Cloud Engineer": [
{"q":"Cloud computing is?","opt":["Online storage","Offline","None"],"ans":"Online storage"},
{"q":"AWS is?","opt":["Cloud platform","Language","Tool"],"ans":"Cloud platform"},
{"q":"Docker is?","opt":["Container tool","Database","UI"],"ans":"Container tool"},
{"q":"Kubernetes is?","opt":["Container management","Coding","Design"],"ans":"Container management"},
{"q":"Virtualization is?","opt":["Virtual system","Real system","None"],"ans":"Virtual system"},
{"q":"Azure is?","opt":["Cloud platform","Game","Tool"],"ans":"Cloud platform"},
{"q":"GCP is?","opt":["Cloud","Database","UI"],"ans":"Cloud"},
{"q":"CI/CD is?","opt":["Automation","Manual","None"],"ans":"Automation"}
],

"UI/UX Designer": [
{"q":"UI means?","opt":["User Interface","User Input","None"],"ans":"User Interface"},
{"q":"UX means?","opt":["User Experience","User Extra","None"],"ans":"User Experience"},
{"q":"Wireframe is?","opt":["Layout","Code","Database"],"ans":"Layout"},
{"q":"Prototype is?","opt":["Model","Final","None"],"ans":"Model"},
{"q":"Figma is?","opt":["Design tool","Language","DB"],"ans":"Design tool"},
{"q":"User research is?","opt":["Study users","Ignore","None"],"ans":"Study users"},
{"q":"Typography is?","opt":["Text design","Image","Code"],"ans":"Text design"},
{"q":"Testing is?","opt":["Check design","Delete","Ignore"],"ans":"Check design"}
],

"Mobile App Developer": [
{"q":"Android SDK is?","opt":["Tool","DB","UI"],"ans":"Tool"},
{"q":"Flutter is?","opt":["Framework","Language","Tool"],"ans":"Framework"},
{"q":"API is?","opt":["Interface","Database","Server"],"ans":"Interface"},
{"q":"Debugging is?","opt":["Fix errors","Create app","Delete"],"ans":"Fix errors"},
{"q":"Kotlin is?","opt":["Language","DB","UI"],"ans":"Language"},
{"q":"Swift is?","opt":["Language","Tool","DB"],"ans":"Language"},
{"q":"React Native is?","opt":["Framework","Language","DB"],"ans":"Framework"},
{"q":"UI means?","opt":["Interface","Code","DB"],"ans":"Interface"}
],

"Game Developer": [
{"q":"Unity is?","opt":["Game engine","Language","DB"],"ans":"Game engine"},
{"q":"Unreal engine is?","opt":["Game engine","Tool","DB"],"ans":"Game engine"},
{"q":"2D game means?","opt":["Flat","3D","None"],"ans":"Flat"},
{"q":"Rendering is?","opt":["Display","Delete","Ignore"],"ans":"Display"},
{"q":"Physics in game?","opt":["Real movement","Fake","None"],"ans":"Real movement"},
{"q":"C# is?","opt":["Language","Tool","DB"],"ans":"Language"},
{"q":"Assets are?","opt":["Resources","Code","DB"],"ans":"Resources"},
{"q":"Animation is?","opt":["Movement","Stop","None"],"ans":"Movement"}
],

"DevOps Engineer": [
{"q":"DevOps is?","opt":["Development+Operations","Design","None"],"ans":"Development+Operations"},
{"q":"CI/CD is?","opt":["Automation","Manual","None"],"ans":"Automation"},
{"q":"Docker is?","opt":["Container","DB","UI"],"ans":"Container"},
{"q":"Jenkins is?","opt":["Tool","Language","DB"],"ans":"Tool"},
{"q":"Terraform is?","opt":["IaC tool","Game","DB"],"ans":"IaC tool"},
{"q":"Monitoring is?","opt":["Track system","Delete","Ignore"],"ans":"Track system"},
{"q":"Logging is?","opt":["Record data","Delete","Ignore"],"ans":"Record data"},
{"q":"AWS used for?","opt":["Cloud","Game","DB"],"ans":"Cloud"}
],

"Blockchain Developer": [
{"q":"Blockchain is?","opt":["Distributed ledger","DB","UI"],"ans":"Distributed ledger"},
{"q":"Smart contract is?","opt":["Auto contract","Manual","None"],"ans":"Auto contract"},
{"q":"Ethereum is?","opt":["Platform","Game","DB"],"ans":"Platform"},
{"q":"Web3 is?","opt":["Decentralized web","Normal web","None"],"ans":"Decentralized web"},
{"q":"Bitcoin is?","opt":["Crypto","Game","DB"],"ans":"Crypto"},
{"q":"Mining is?","opt":["Validation","Delete","Ignore"],"ans":"Validation"},
{"q":"Gas fee is?","opt":["Transaction fee","Free","None"],"ans":"Transaction fee"},
{"q":"DeFi is?","opt":["Finance","Game","DB"],"ans":"Finance"}
],

"Data Analyst": [
    {"question": "Which tool is used for data visualization?", "options": ["Excel", "Tableau", "Word", "Photoshop"], "answer": "Tableau"},
    {"question": "Which language is used for analysis?", "options": ["Python", "HTML", "CSS", "C"], "answer": "Python"},
    {"question": "What is SQL used for?", "options": ["Database queries", "Styling", "Design", "Animation"], "answer": "Database queries"},
    {"question": "Which tool is used for dashboards?", "options": ["Power BI", "React", "Node", "Figma"], "answer": "Power BI"},
    {"question": "What is data cleaning?", "options": ["Removing errors", "Writing code", "Designing UI", "Deployment"], "answer": "Removing errors"},
    {"question": "Which file format is common for datasets?", "options": ["CSV", "HTML", "MP3", "PNG"], "answer": "CSV"},
    {"question": "What is pivot table used for?", "options": ["Summarizing data", "Coding", "Designing", "Testing"], "answer": "Summarizing data"},
    {"question": "Which library is used in Python?", "options": ["Pandas", "React", "Bootstrap", "Node"], "answer": "Pandas"},
    {"question": "What is data visualization?", "options": ["Graphical representation", "Coding", "Testing", "Deployment"], "answer": "Graphical representation"},
    {"question": "Which skill is important?", "options": ["Analytical thinking", "Painting", "Singing", "Driving"], "answer": "Analytical thinking"}
],


"Machine Learning Engineer": [
    {"question": "What is ML?", "options": ["Machine Learning", "Markup Language", "Main Logic", "None"], "answer": "Machine Learning"},
    {"question": "Which library is used?", "options": ["Scikit-learn", "Bootstrap", "HTML", "CSS"], "answer": "Scikit-learn"},
    {"question": "What is training data?", "options": ["Data to train model", "UI data", "CSS data", "None"], "answer": "Data to train model"},
    {"question": "Which framework is used?", "options": ["TensorFlow", "React", "Angular", "Vue"], "answer": "TensorFlow"},
    {"question": "What is model?", "options": ["Algorithm output", "UI", "Database", "None"], "answer": "Algorithm output"},
    {"question": "What is prediction?", "options": ["Output from model", "Design", "Code", "Test"], "answer": "Output from model"},
    {"question": "Which field uses ML?", "options": ["AI", "Design", "Web", "Testing"], "answer": "AI"},
    {"question": "What is overfitting?", "options": ["Too specific model", "UI error", "Network issue", "None"], "answer": "Too specific model"},
    {"question": "Which language is common?", "options": ["Python", "HTML", "CSS", "SQL"], "answer": "Python"},
    {"question": "Which skill is needed?", "options": ["Math", "Drawing", "Singing", "Driving"], "answer": "Math"}
],


"Software Engineer": [
    {"question": "What is DSA?", "options": ["Data Structures & Algorithms", "Design System App", "None", "Other"], "answer": "Data Structures & Algorithms"},
    {"question": "Which language is OOP?", "options": ["Java", "HTML", "CSS", "SQL"], "answer": "Java"},
    {"question": "What is Git?", "options": ["Version control", "Database", "UI tool", "Game"], "answer": "Version control"},
    {"question": "What is debugging?", "options": ["Fixing errors", "Designing", "Testing", "Deploying"], "answer": "Fixing errors"},
    {"question": "What is API?", "options": ["Communication interface", "UI", "CSS", "None"], "answer": "Communication interface"},
    {"question": "Which concept is OOP?", "options": ["Inheritance", "Color", "Design", "Layout"], "answer": "Inheritance"},
    {"question": "Which tool is used?", "options": ["VS Code", "Photoshop", "Excel", "Word"], "answer": "VS Code"},
    {"question": "What is backend?", "options": ["Server side", "UI", "Design", "Testing"], "answer": "Server side"},
    {"question": "Which skill matters?", "options": ["Problem solving", "Singing", "Dancing", "Painting"], "answer": "Problem solving"},
    {"question": "What is deployment?", "options": ["Launching app", "Coding", "Testing", "Design"], "answer": "Launching app"}
],


"System Administrator": [
    {"question": "Which OS is used?", "options": ["Linux", "Paint", "Excel", "Word"], "answer": "Linux"},
    {"question": "What is server?", "options": ["Service provider system", "UI", "Code", "None"], "answer": "Service provider system"},
    {"question": "What is shell?", "options": ["Command interface", "UI", "Design", "None"], "answer": "Command interface"},
    {"question": "What is networking?", "options": ["Connecting systems", "Coding", "Design", "Testing"], "answer": "Connecting systems"},
    {"question": "Which command is used?", "options": ["ls", "html", "css", "figma"], "answer": "ls"},
    {"question": "What is backup?", "options": ["Data copy", "UI", "Code", "None"], "answer": "Data copy"},
    {"question": "Which skill?", "options": ["Troubleshooting", "Drawing", "Music", "Dance"], "answer": "Troubleshooting"},
    {"question": "What is IP?", "options": ["Address", "Code", "UI", "None"], "answer": "Address"},
    {"question": "What is firewall?", "options": ["Security system", "UI", "Code", "None"], "answer": "Security system"},
    {"question": "What is scripting?", "options": ["Automation", "Design", "Testing", "None"], "answer": "Automation"}
],


"Software Tester": [
    {"question": "What is testing?", "options": ["Finding bugs", "Coding", "Designing", "Deploying"], "answer": "Finding bugs"},
    {"question": "What is QA?", "options": ["Quality Assurance", "Code", "UI", "None"], "answer": "Quality Assurance"},
    {"question": "Which tool?", "options": ["Selenium", "React", "Node", "MongoDB"], "answer": "Selenium"},
    {"question": "What is bug?", "options": ["Error", "UI", "Code", "None"], "answer": "Error"},
    {"question": "What is test case?", "options": ["Scenario", "Code", "Design", "None"], "answer": "Scenario"},
    {"question": "What is automation?", "options": ["Automatic testing", "UI", "Code", "None"], "answer": "Automatic testing"},
    {"question": "Which skill?", "options": ["Attention to detail", "Drawing", "Music", "Dance"], "answer": "Attention to detail"},
    {"question": "What is regression?", "options": ["Retesting", "Coding", "Design", "None"], "answer": "Retesting"},
    {"question": "What is manual testing?", "options": ["Human testing", "AI", "Robot", "None"], "answer": "Human testing"},
    {"question": "What is defect?", "options": ["Bug", "UI", "Code", "None"], "answer": "Bug"}
],


"AR/VR Developer": [
    {"question": "What is VR?", "options": ["Virtual Reality", "Variable Rate", "None", "Other"], "answer": "Virtual Reality"},
    {"question": "Which tool?", "options": ["Unity", "Excel", "SQL", "Word"], "answer": "Unity"},
    {"question": "Which language?", "options": ["C#", "HTML", "CSS", "SQL"], "answer": "C#"},
    {"question": "What is AR?", "options": ["Augmented Reality", "AI", "App", "None"], "answer": "Augmented Reality"},
    {"question": "What is 3D?", "options": ["3 Dimensions", "2D", "1D", "None"], "answer": "3 Dimensions"},
    {"question": "Which engine?", "options": ["Unreal", "React", "Node", "Mongo"], "answer": "Unreal"},
    {"question": "What is rendering?", "options": ["Image creation", "Code", "UI", "None"], "answer": "Image creation"},
    {"question": "What is headset?", "options": ["VR device", "Mouse", "Keyboard", "None"], "answer": "VR device"},
    {"question": "Which skill?", "options": ["Creativity", "Singing", "Driving", "None"], "answer": "Creativity"},
    {"question": "What is simulation?", "options": ["Virtual environment", "Code", "UI", "None"], "answer": "Virtual environment"}
],


"Embedded Engineer": [
    {"question": "Which language?", "options": ["C", "HTML", "CSS", "SQL"], "answer": "C"},
    {"question": "What is microcontroller?", "options": ["Small computer", "UI", "Code", "None"], "answer": "Small computer"},
    {"question": "What is Arduino?", "options": ["Board", "Database", "Framework", "None"], "answer": "Board"},
    {"question": "What is IoT?", "options": ["Internet of Things", "Code", "UI", "None"], "answer": "Internet of Things"},
    {"question": "What is sensor?", "options": ["Input device", "Output", "UI", "None"], "answer": "Input device"},
    {"question": "What is circuit?", "options": ["Electrical path", "Code", "UI", "None"], "answer": "Electrical path"},
    {"question": "What is firmware?", "options": ["Embedded software", "UI", "Code", "None"], "answer": "Embedded software"},
    {"question": "Which skill?", "options": ["Problem solving", "Drawing", "Music", "None"], "answer": "Problem solving"},
    {"question": "What is debugging?", "options": ["Fixing errors", "Design", "Testing", "None"], "answer": "Fixing errors"},
    {"question": "What is PCB?", "options": ["Circuit board", "UI", "Code", "None"], "answer": "Circuit board"}
],


"Network Engineer": [
    {"question": "What is TCP/IP?", "options": ["Protocol", "Language", "UI", "None"], "answer": "Protocol"},
    {"question": "What is router?", "options": ["Network device", "Mouse", "Keyboard", "None"], "answer": "Network device"},
    {"question": "What is LAN?", "options": ["Local Area Network", "App", "Code", "None"], "answer": "Local Area Network"},
    {"question": "What is IP?", "options": ["Address", "Code", "UI", "None"], "answer": "Address"},
    {"question": "What is DNS?", "options": ["Domain system", "UI", "Code", "None"], "answer": "Domain system"},
    {"question": "What is switch?", "options": ["Network device", "UI", "Code", "None"], "answer": "Network device"},
    {"question": "What is firewall?", "options": ["Security", "UI", "Code", "None"], "answer": "Security"},
    {"question": "Which skill?", "options": ["Logical thinking", "Drawing", "Music", "None"], "answer": "Logical thinking"},
    {"question": "What is WAN?", "options": ["Wide Area Network", "Code", "UI", "None"], "answer": "Wide Area Network"},
    {"question": "What is packet?", "options": ["Data unit", "UI", "Code", "None"], "answer": "Data unit"}
],


"Technical Support Engineer": [
    {"question": "What is troubleshooting?", "options": ["Fixing issues", "Coding", "Designing", "None"], "answer": "Fixing issues"},
    {"question": "Which OS?", "options": ["Windows", "Photoshop", "Excel", "None"], "answer": "Windows"},
    {"question": "What is helpdesk?", "options": ["Support system", "Code", "UI", "None"], "answer": "Support system"},
    {"question": "What is hardware?", "options": ["Physical parts", "Code", "UI", "None"], "answer": "Physical parts"},
    {"question": "What is software?", "options": ["Programs", "UI", "Code", "None"], "answer": "Programs"},
    {"question": "Which skill?", "options": ["Communication", "Drawing", "Music", "None"], "answer": "Communication"},
    {"question": "What is network issue?", "options": ["Connection problem", "UI", "Code", "None"], "answer": "Connection problem"},
    {"question": "What is OS?", "options": ["Operating system", "Code", "UI", "None"], "answer": "Operating system"},
    {"question": "What is update?", "options": ["Upgrade system", "UI", "Code", "None"], "answer": "Upgrade system"},
    {"question": "What is support ticket?", "options": ["Issue record", "UI", "Code", "None"], "answer": "Issue record"}
],


"Product Manager": [
    {"question": "What is Agile?", "options": ["Methodology", "Language", "UI", "None"], "answer": "Methodology"},
    {"question": "What is Scrum?", "options": ["Framework", "Code", "UI", "None"], "answer": "Framework"},
    {"question": "What is roadmap?", "options": ["Product plan", "Code", "UI", "None"], "answer": "Product plan"},
    {"question": "What is sprint?", "options": ["Work cycle", "Run", "Code", "None"], "answer": "Work cycle"},
    {"question": "What is backlog?", "options": ["Task list", "Code", "UI", "None"], "answer": "Task list"},
    {"question": "Which skill?", "options": ["Leadership", "Drawing", "Music", "None"], "answer": "Leadership"},
    {"question": "What is KPI?", "options": ["Performance metric", "UI", "Code", "None"], "answer": "Performance metric"},
    {"question": "What is user story?", "options": ["User requirement", "Code", "UI", "None"], "answer": "User requirement"},
    {"question": "What is MVP?", "options": ["Minimum product", "Code", "UI", "None"], "answer": "Minimum product"},
    {"question": "What is stakeholder?", "options": ["Interested party", "UI", "Code", "None"], "answer": "Interested party"}
]


}
def normalize_question(q):
    return {
        "q": q.get("q") or q.get("question"),
        "opt": q.get("opt") or q.get("options"),
        "ans": q.get("ans") or q.get("answer")
    }


def get_random_questions(career):
    questions = quiz_data.get(career, [])
    
    # normalize all questions
    normalized = [normalize_question(q) for q in questions]

    return random.sample(normalized, min(7, len(normalized)))
