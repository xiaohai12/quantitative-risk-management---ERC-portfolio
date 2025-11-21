import re
import streamlit as st
import utils.web_util as wu

st.set_page_config(page_title="Contact Us", page_icon="📬")

# Custom style
wu.apply_custom_css()
# Nav bar
wu.render_navbar()

# ---- GLOBAL STYLE (background + card feeling) ----
st.markdown("""
<style>
    /* Fond bleu foncé premium */
    .stApp {
        background-color: #0A1B3F;   /* bleu foncé élégant */
    }

    /* Contenu central (carte blanche) */
    .block-container {
        background-color: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 0 25px rgba(0,0,0,0.30);
    }
</style>
""", unsafe_allow_html=True)




# ---- HEADER ----
st.title("📬 Contact Us")

st.write(
    """
    **We’d be happy to hear from you.**

    Whether you have a question about our risk budgeting approach,
    need help understanding your Equal Risk Contribution (ERC) allocation,
    or are facing a technical issue, we’re here to help.

    Fill out the form below and our team will get back to you as soon as possible.  
    We usually reply within **24–48 hours**.
    """
)

st.markdown("---")

# ---- COUNTRY CODES (tous les pays) ----
country_codes = {
    "Afghanistan (+93)": "+93",
    "Albania (+355)": "+355",
    "Algeria (+213)": "+213",
    "Andorra (+376)": "+376",
    "Angola (+244)": "+244",
    "Antigua and Barbuda (+1-268)": "+1-268",
    "Argentina (+54)": "+54",
    "Armenia (+374)": "+374",
    "Australia (+61)": "+61",
    "Austria (+43)": "+43",
    "Azerbaijan (+994)": "+994",
    "Bahamas (+1-242)": "+1-242",
    "Bahrain (+973)": "+973",
    "Bangladesh (+880)": "+880",
    "Barbados (+1-246)": "+1-246",
    "Belarus (+375)": "+375",
    "Belgium (+32)": "+32",
    "Belize (+501)": "+501",
    "Benin (+229)": "+229",
    "Bhutan (+975)": "+975",
    "Bolivia (+591)": "+591",
    "Bosnia and Herzegovina (+387)": "+387",
    "Botswana (+267)": "+267",
    "Brazil (+55)": "+55",
    "Brunei (+673)": "+673",
    "Bulgaria (+359)": "+359",
    "Burkina Faso (+226)": "+226",
    "Burundi (+257)": "+257",
    "Cabo Verde (+238)": "+238",
    "Cambodia (+855)": "+855",
    "Cameroon (+237)": "+237",
    "Canada (+1)": "+1",
    "Central African Republic (+236)": "+236",
    "Chad (+235)": "+235",
    "Chile (+56)": "+56",
    "China (+86)": "+86",
    "Colombia (+57)": "+57",
    "Comoros (+269)": "+269",
    "Congo, Republic (+242)": "+242",
    "Congo, DR (+243)": "+243",
    "Costa Rica (+506)": "+506",
    "Croatia (+385)": "+385",
    "Cuba (+53)": "+53",
    "Cyprus (+357)": "+357",
    "Czech Republic (+420)": "+420",
    "Denmark (+45)": "+45",
    "Djibouti (+253)": "+253",
    "Dominica (+1-767)": "+1-767",
    "Dominican Republic (+1-809)": "+1-809",
    "Ecuador (+593)": "+593",
    "Egypt (+20)": "+20",
    "El Salvador (+503)": "+503",
    "Equatorial Guinea (+240)": "+240",
    "Eritrea (+291)": "+291",
    "Estonia (+372)": "+372",
    "Eswatini (+268)": "+268",
    "Ethiopia (+251)": "+251",
    "Fiji (+679)": "+679",
    "Finland (+358)": "+358",
    "France (+33)": "+33",
    "Gabon (+241)": "+241",
    "Gambia (+220)": "+220",
    "Georgia (+995)": "+995",
    "Germany (+49)": "+49",
    "Ghana (+233)": "+233",
    "Greece (+30)": "+30",
    "Grenada (+1-473)": "+1-473",
    "Guatemala (+502)": "+502",
    "Guinea (+224)": "+224",
    "Guinea-Bissau (+245)": "+245",
    "Guyana (+592)": "+592",
    "Haiti (+509)": "+509",
    "Honduras (+504)": "+504",
    "Hungary (+36)": "+36",
    "Iceland (+354)": "+354",
    "India (+91)": "+91",
    "Indonesia (+62)": "+62",
    "Iran (+98)": "+98",
    "Iraq (+964)": "+964",
    "Ireland (+353)": "+353",
    "Israel (+972)": "+972",
    "Italy (+39)": "+39",
    "Jamaica (+1-876)": "+1-876",
    "Japan (+81)": "+81",
    "Jordan (+962)": "+962",
    "Kazakhstan (+7)": "+7",
    "Kenya (+254)": "+254",
    "Kiribati (+686)": "+686",
    "Korea, North (+850)": "+850",
    "Korea, South (+82)": "+82",
    "Kosovo (+383)": "+383",
    "Kuwait (+965)": "+965",
    "Kyrgyzstan (+996)": "+996",
    "Laos (+856)": "+856",
    "Latvia (+371)": "+371",
    "Lebanon (+961)": "+961",
    "Lesotho (+266)": "+266",
    "Liberia (+231)": "+231",
    "Libya (+218)": "+218",
    "Liechtenstein (+423)": "+423",
    "Lithuania (+370)": "+370",
    "Luxembourg (+352)": "+352",
    "Madagascar (+261)": "+261",
    "Malawi (+265)": "+265",
    "Malaysia (+60)": "+60",
    "Maldives (+960)": "+960",
    "Mali (+223)": "+223",
    "Malta (+356)": "+356",
    "Marshall Islands (+692)": "+692",
    "Mauritania (+222)": "+222",
    "Mauritius (+230)": "+230",
    "Mexico (+52)": "+52",
    "Micronesia (+691)": "+691",
    "Moldova (+373)": "+373",
    "Monaco (+377)": "+377",
    "Mongolia (+976)": "+976",
    "Montenegro (+382)": "+382",
    "Morocco (+212)": "+212",
    "Mozambique (+258)": "+258",
    "Myanmar (+95)": "+95",
    "Namibia (+264)": "+264",
    "Nauru (+674)": "+674",
    "Nepal (+977)": "+977",
    "Netherlands (+31)": "+31",
    "New Zealand (+64)": "+64",
    "Nicaragua (+505)": "+505",
    "Niger (+227)": "+227",
    "Nigeria (+234)": "+234",
    "North Macedonia (+389)": "+389",
    "Norway (+47)": "+47",
    "Oman (+968)": "+968",
    "Pakistan (+92)": "+92",
    "Palau (+680)": "+680",
    "Panama (+507)": "+507",
    "Papua New Guinea (+675)": "+675",
    "Paraguay (+595)": "+595",
    "Peru (+51)": "+51",
    "Philippines (+63)": "+63",
    "Poland (+48)": "+48",
    "Portugal (+351)": "+351",
    "Qatar (+974)": "+974",
    "Romania (+40)": "+40",
    "Russia (+7)": "+7",
    "Rwanda (+250)": "+250",
    "Saint Kitts and Nevis (+1-869)": "+1-869",
    "Saint Lucia (+1-758)": "+1-758",
    "Saint Vincent (+1-784)": "+1-784",
    "Samoa (+685)": "+685",
    "San Marino (+378)": "+378",
    "Sao Tome and Principe (+239)": "+239",
    "Saudi Arabia (+966)": "+966",
    "Senegal (+221)": "+221",
    "Serbia (+381)": "+381",
    "Seychelles (+248)": "+248",
    "Sierra Leone (+232)": "+232",
    "Singapore (+65)": "+65",
    "Slovakia (+421)": "+421",
    "Slovenia (+386)": "+386",
    "Solomon Islands (+677)": "+677",
    "Somalia (+252)": "+252",
    "South Africa (+27)": "+27",
    "South Sudan (+211)": "+211",
    "Sri Lanka (+94)": "+94",
    "Sudan (+249)": "+249",
    "Suriname (+597)": "+597",
    "Sweden (+46)": "+46",
    "Switzerland (+41)": "+41",
    "Syria (+963)": "+963",
    "Taiwan (+886)": "+886",
    "Tajikistan (+992)": "+992",
    "Tanzania (+255)": "+255",
    "Thailand (+66)": "+66",
    "Timor-Leste (+670)": "+670",
    "Togo (+228)": "+228",
    "Tonga (+676)": "+676",
    "Trinidad and Tobago (+1-868)": "+1-868",
    "Tunisia (+216)": "+216",
    "Turkey (+90)": "+90",
    "Turkmenistan (+993)": "+993",
    "Tuvalu (+688)": "+688",
    "Uganda (+256)": "+256",
    "Ukraine (+380)": "+380",
    "United Arab Emirates (+971)": "+971",
    "United Kingdom (+44)": "+44",
    "United States (+1)": "+1",
    "Uruguay (+598)": "+598",
    "Uzbekistan (+998)": "+998",
    "Vanuatu (+678)": "+678",
    "Vatican City (+39)": "+39",
    "Venezuela (+58)": "+58",
    "Vietnam (+84)": "+84",
    "Yemen (+967)": "+967",
    "Zambia (+260)": "+260",
    "Zimbabwe (+263)": "+263",
}

# ---- CONTACT FORM ----
with st.form("contact_form"):

    # SECTION 1 - Your information
    st.subheader("Your information")

    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Name")
    with col2:
        email = st.text_input("Email")

    st.markdown("**Phone number (optional)**")

    colA, colB = st.columns([1.2, 2])
    with colA:
        country_list = list(country_codes.keys())
        default_index = country_list.index("Switzerland (+41)") if "Switzerland (+41)" in country_list else 0
        country = st.selectbox("Country", country_list, index=default_index)
    with colB:
        local_number = st.text_input("Local number (without country code)")

    full_phone = None
    if local_number.strip():
        full_phone = f"{country_codes[country]} {local_number.strip()}"

    # SECTION 2 - Your request
    st.subheader("Your request")

    topic = st.selectbox(
        "What is your request about?",
        [
            "Question about the platform",
            "Technical issue / bug",
            "ERC / risk budgeting question",
            "Feature suggestion",
            "Collaboration request",
            "Other",
        ],
    )

    message = st.text_area(
        "Message",
        placeholder="Tell us how we can help you...",
        height=200,
    )

    # SECTION 3 - Attachments (optional)
    st.subheader("Attachments (optional)")
    attachment = st.file_uploader(
        "Attach a file (e.g. screenshot, PDF) to help us understand your request (optional)",
        type=["png", "jpg", "jpeg", "pdf"],
    )

    # SECTION 4 - Consent
    st.subheader("Privacy & consent")
    consent = st.checkbox(
        "I agree that my information may be used to respond to my request."
    )

    # ---- Submit ----
    submitted = st.form_submit_button("Submit")

    # Petit texte d’info sous le bouton
    st.caption(
        "Once submitted, your message will be forwarded to our team automatically. "
        "You will receive a confirmation email if your request has been successfully recorded."
    )

    # ---- Logic après submit ----
    if submitted:
        email_pattern = r"^[^@]+@[^@]+\.[^@]+$"

        if not name or not email or not message:
            st.error("Please fill in your **Name**, **Email**, and **Message**.")
        elif not re.match(email_pattern, email):
            st.error("Please enter a valid email address.")
        elif not consent:
            st.warning("You must accept the consent box to submit.")
        else:
            # Confirmation premium
            st.success("✅ Your request has been successfully recorded.")

            st.markdown(
                """
                <div style="border-radius:10px;padding:1rem;margin-top:0.5rem;
                            background-color:#F0F9FF;border:1px solid #BFDBFE;">
                    <h4 style="margin:0 0 0.3rem 0;">🎉 Message sent!</h4>
                    <p style="margin:0;">
                        Thank you for reaching out. Our team will review your message and get back to you
                        within <strong>24–48 hours</strong>.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            with st.expander("See your submitted information"):
                st.write(f"**Name:** {name}")
                st.write(f"**Email:** {email}")
                if full_phone:
                    st.write(f"**Phone:** {full_phone}")
                st.write(f"**Topic:** {topic}")
                st.write("**Message:**")
                st.write(message)
                if attachment is not None:
                    st.write(f"**Attachment uploaded:** {attachment.name}")
                else:
                    st.write("**Attachment uploaded:** None")

# ---- FAQ SECTION ----
st.markdown("---")
st.markdown("### FAQ")

with st.expander("How does ERC (Equal Risk Contribution) allocation work?"):
    st.write(
        "In an ERC portfolio, each asset (or risk factor) is scaled so that it contributes "
        "the same amount of risk to the total portfolio. This is typically measured using "
        "volatility and correlations, based on the covariance matrix of asset returns."
    )

with st.expander("How do you treat bonds, commodities, and crypto in the portfolio?"):
    st.write(
        "All asset classes are integrated in a unified risk framework. Bonds, commodities, "
        "and crypto assets are included through their historical return and volatility, "
        "so that the ERC engine can allocate risk consistently across them."
    )

with st.expander("Is this platform giving me investment advice?"):
    st.write(
        "No. The platform provides analytics and tools based on risk budgeting and ERC. "
        "It is designed for educational and analytical purposes and does not provide "
        "personalized investment advice."
    )

with st.expander("What should I include in my message for technical issues?"):
    st.write(
        "If you are facing a bug or technical issue, please include a short description, "
        "the steps to reproduce it, and optionally a screenshot or PDF attachment using "
        "the upload field in the form."
    )

# ---- FOOTER / DISCLAIMER ----
st.markdown("---")
st.caption(
    "Important: This platform does not provide personalized investment advice. "
    "All allocations and analytics are for educational and informational purposes only. "
    "Thank you for your interest — we look forward to helping you build more robust, "
    "diversified portfolios through risk-based allocation."
)
