import streamlit as st
from PIL import Image
from datetime import date
import urllib.parse
from openai import OpenAI
import base64
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="PawPal AI 🐾", layout="wide")

# ================= PREMIUM UI =================
st.markdown("""
<style>
body {background-color:#0e1117;}
.card {
    background:linear-gradient(145deg,#1e1e1e,#2b2b2b);
    padding:25px;
    border-radius:20px;
    box-shadow:0 0 25px rgba(255,255,255,0.05);
    animation: fadeIn 0.6s ease-in-out;
}
@keyframes fadeIn {
    from {opacity:0; transform:translateY(10px);}
    to {opacity:1;}
}
</style>
""", unsafe_allow_html=True)

# ================= SESSION =================
if "pet" not in st.session_state:
    st.session_state.pet = {}
if "pet_image" not in st.session_state:
    st.session_state.pet_image = None
if "selected_symptoms" not in st.session_state:
    st.session_state.selected_symptoms = []
if "final_report" not in st.session_state:
    st.session_state.final_report = ""

# ================= NAV =================
page = st.sidebar.radio("🐾 Navigate", [
    "Pet Profile 🐾",
    "Symptom Checker 🧠",
    "PetGPT 🤖",
    "Image Analysis 🖼",
    "Vet Finder 📍",
    "Report 📄"
])

# ================= WEIGHT STATUS =================
def get_weight_status(species, weight):
    if species == "Dog":
        return "Underweight" if weight < 5 else "Normal" if weight < 25 else "Overweight" if weight < 40 else "Obese"
    elif species == "Cat":
        return "Underweight" if weight < 3 else "Normal" if weight <= 5 else "Overweight" if weight <= 7 else "Obese"
    elif species == "Guinea Pig":
        return "Underweight" if weight < 0.7 else "Normal" if weight <= 1.2 else "Overweight"
    elif species == "Hamster":
        return "Underweight" if weight < 0.08 else "Normal" if weight <= 0.15 else "Overweight"
    else:
        return "Consult vet"

# =====================================================
# 🐾 PET PROFILE
# =====================================================
if page == "Pet Profile 🐾":

    st.title("🐾 Pet Profile")

    name = st.text_input("Pet Name")
    species = st.selectbox("Species", ["Dog","Cat","Fish","Bird","Rabbit","Hamster","Guinea Pig","Other"])
    breed = st.text_input("Breed")

    col1, col2 = st.columns(2)
    with col1:
        y = st.number_input("Years", 0, 50)
    with col2:
        m = st.number_input("Months", 0, 11)

    col1, col2 = st.columns([2,1])
    with col1:
        weight = st.number_input("⚖️ Weight", min_value=0.0, step=0.1)
    with col2:
        unit = st.selectbox("Unit", ["kg","lbs"])

    weight_kg = weight * 0.453592 if unit == "lbs" else weight

    gender = st.selectbox("Gender", ["Male","Female","Unknown"])
    vacc = st.selectbox("Vaccination", ["Up to date","Not sure","Not vaccinated"])
    diet = st.selectbox("Diet", ["Dry","Wet","Homemade","Mixed"])

    medical = st.text_area("Medical History")
    visit = st.date_input("Last Vet Visit", max_value=date.today())

    img_file = st.file_uploader("Upload Pet Image", type=["jpg","png","jpeg"])

    if st.button("Save"):
        if img_file:
            st.session_state.pet_image = Image.open(img_file)

        st.session_state.pet = {
            "name": name,
            "species": species,
            "breed": breed,
            "age": f"{y}y {m}m",
            "weight": weight_kg,
            "gender": gender,
            "vacc": vacc,
            "diet": diet,
            "medical": medical,
            "visit": str(visit)
        }

        st.success("✅ Profile Saved!")

# =====================================================
# 🧠 SYMPTOM CHECKER
# =====================================================
elif page == "Symptom Checker 🧠":

    st.title("🧠 Symptom Checker")

    if not st.session_state.pet:
        st.warning("Create profile first")
        st.stop()

    pet = st.session_state.pet

    # ================= WEIGHT =================
    status = get_weight_status(pet["species"], pet["weight"])
    st.info(f"⚖️ Weight Status: {status}")

    # ================= SMART SYMPTOMS =================
    if pet["species"] == "Dog":
        symptoms = [
            "Vomiting 🤮", "Diarrhea 💩", "Excess barking 🐕",
            "Limping 🦴", "Loss of appetite 🍽", "Weight loss ⚖️",
            "Hair loss 🐾", "Skin infection 🩹", "Fever 🌡",
            "Coughing 😷", "Sneezing 🤧", "Aggression 😠",
            "Lethargy 😴", "Eye discharge 👁", "Ear scratching 👂"
        ]

    elif pet["species"] == "Cat":
        symptoms = [
            "Hairball 😼", "Vomiting 🤮", "Hiding 😿",
            "Scratching 🐾", "Loss of appetite 🍽", "Weight loss ⚖️",
            "Eye infection 👁", "Aggression 😾", "Lethargy 😴",
            "Excess grooming 🧼", "Fever 🌡", "Sneezing 🤧",
            "Breathing issues 😮‍💨", "Ear mites 👂"
        ]

    elif pet["species"] == "Fish":
        symptoms = [
            "Floating sideways 🐟", "White spots ⚪",
            "Not swimming 🚫", "Gasping at surface 😮",
            "Color fading 🎨", "Fins damaged 🪶",
            "Loss of balance ⚖️", "Cloudy eyes 👁",
            "Rapid breathing 💨"
        ]

    elif pet["species"] == "Bird":
        symptoms = [
            "Feather loss 🪶", "Not chirping 🔇",
            "Weakness 😴", "Breathing issue 😮‍💨",
            "Loss of balance ⚖️", "Eye discharge 👁",
            "Swollen feet 🦶", "Loss of appetite 🍽",
            "Fluffed feathers 🐦"
        ]

    elif pet["species"] == "Rabbit":
        symptoms = [
            "Not eating 🍽", "Teeth grinding 🦷",
            "Lethargy 😴", "Runny nose 🤧",
            "Hair loss 🐾", "Diarrhea 💩",
            "Ear infection 👂", "Weight loss ⚖️"
        ]

    elif pet["species"] == "Hamster":
        symptoms = [
            "Wet tail 💩", "Not moving 🚫",
            "Weight loss ⚖️", "Hair loss 🐾",
            "Swelling 🤕", "Eye infection 👁",
            "Lethargy 😴", "Loss of appetite 🍽"
        ]

    elif pet["species"] == "Guinea Pig":
        symptoms = [
            "Scurvy signs (weakness) 🍊", "Hair loss 🐾",
            "Not eating 🍽", "Weight loss ⚖️",
            "Eye infection 👁", "Breathing issues 😮‍💨",
            "Limping 🦴", "Diarrhea 💩"
        ]

    else:
        symptoms = [
            "Weakness 😴", "Loss of appetite 🍽",
            "Lethargy 😴", "Weight loss ⚖️",
            "Fever 🌡", "Behavior change 🤔"
        ]

    # ================= UI =================
    selected = st.multiselect(
        "🧠 Select Symptoms",
        symptoms,
        help="Choose all visible symptoms for better diagnosis"
    )

    # ================= SMART DIAGNOSIS =================
    if st.button("Analyze"):

        if not selected:
            st.warning("Select symptoms first")
            st.stop()

        st.session_state.selected_symptoms = selected

        prompt = f"""
        You are a veterinary AI.

        Pet: {pet}
        Symptoms: {selected}

        Give STRICT format:

        Disease:
        Severity (Low/Medium/High):
        Confidence (%):
        Explanation:
        Advice:
        Emergency (Yes/No):
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role":"user","content":prompt}]
        )

        result = response.choices[0].message.content
        st.session_state.final_report = result

        st.markdown("### 🧠 AI Diagnosis")

        if "High" in result or "Emergency: Yes" in result:
            st.error(result)
            st.markdown("### 🚨 Emergency Attention Required!")
        elif "Medium" in result:
            st.warning(result)
            st.markdown("### ⚠️ Monitor Carefully")
        else:
            st.success(result)
            st.markdown("### ✅ Mild Condition")

 # =====================================================
# 🤖 PETGPT (SMART CHAT UI)
# =====================================================
elif page == "PetGPT 🤖":

    st.title("🤖 PetGPT Assistant")

    # initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # show previous messages
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # user input
    user_input = st.chat_input("Ask anything about your pet...")

    if user_input:

        # show user message
        st.chat_message("user").write(user_input)

        st.session_state.chat_history.append({
            "role": "user",
            "content": user_input
        })

        # add pet context (VERY SMART 🔥)
        pet_context = st.session_state.get("pet", {})

        prompt = f"""
        You are PetGPT, a friendly veterinary assistant.

        Pet Details:
        {pet_context}

        User Question:
        {user_input}

        Give helpful, simple, and caring advice.
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        reply = response.choices[0].message.content

        # show assistant reply
        with st.chat_message("assistant"):
            st.write(reply)

        st.session_state.chat_history.append({
            "role": "assistant",
            "content": reply
        })

# =====================================================
# 🖼 IMAGE ANALYSIS (FIXED)
# =====================================================
elif page == "Image Analysis 🖼":

    st.title("🖼 Image Analysis")

    file = st.file_uploader("Upload Image")

    if file:
        img = Image.open(file)
        st.image(img)

        if st.button("Analyze Image"):

            file_bytes = file.read()
            base64_image = base64.b64encode(file_bytes).decode("utf-8")
            mime = file.type

            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{
                    "role":"user",
                    "content":[
                        {"type":"text","text":"Analyze pet health issues"},
                        {"type":"image_url","image_url":{"url":f"data:{mime};base64,{base64_image}"}}
                    ]
                }]
            )

            res = response.choices[0].message.content
            st.success(res)

            st.session_state.final_report = res

# =====================================================
# 📍 VET FINDER
# =====================================================
elif page == "Vet Finder 📍":

    loc = st.text_input("Location")
    if loc:
        q = urllib.parse.quote(f"vet near {loc}")
        st.markdown(f"[Open Maps](https://google.com/maps/search/{q})")

# =====================================================
# 📄 REPORT
# =====================================================
elif page == "Report 📄":

    if not st.session_state.pet:
        st.warning("No profile")
        st.stop()

    pet = st.session_state.pet

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.markdown(f"## 🐾 {pet['name']}")

    if st.session_state.pet_image:
        st.image(st.session_state.pet_image, width=250)

    st.write(f"Species: {pet['species']}")
    st.write(f"Weight: {pet['weight']} kg")
    st.write(f"Weight Status: {get_weight_status(pet['species'], pet['weight'])}")

    st.write("### Symptoms")
    for s in st.session_state.selected_symptoms:
        st.write(f"- {s}")

    st.write("### Diagnosis")
    st.info(st.session_state.final_report)

    st.markdown('</div>', unsafe_allow_html=True)

    # PDF
    def create_pdf():
        doc = SimpleDocTemplate("report.pdf")
        styles = getSampleStyleSheet()
        content = []

        content.append(Paragraph("PawPal Report", styles["Title"]))
        content.append(Spacer(1,10))
        content.append(Paragraph(f"Name: {pet['name']}", styles["Normal"]))
        content.append(Paragraph(f"Weight Status: {get_weight_status(pet['species'], pet['weight'])}", styles["Normal"]))
        content.append(Paragraph(st.session_state.final_report, styles["Normal"]))

        doc.build(content)
        return "report.pdf"

    if st.button("Generate PDF"):
        file = create_pdf()
        with open(file,"rb") as f:
            st.download_button("Download PDF", f)
