import easyocr
import mysql.connector as sql
from easyocr import Reader
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import matplotlib.pyplot as plt
import cv2
import os
import re

#st.write("## :green[About :] Bizcard")
#st.write(":red[JERRY]")
mydb = sql.connect(host="localhost",
                    user="root",
                    password="mysql@123",
                    database="biscard"
                    )
mycursor = mydb.cursor(buffered=True)

create_table_query="""CREATE TABLE IF NOT EXISTS card_details1(
                        Company_Name varchar(30),
                        Card_Holder_Name varchar(30),
                        Designation varchar(30),
                        Mobile_Number Varchar(15),
                        Email_Id varchar(255),
                        Website varchar(100),
                        Street varchar(50),
                        District varchar(50),
                        State varchar(30),
                        Pincode varchar(10)
    
                        )"""


reader = easyocr.Reader(['en'])

st.set_page_config(page_title=" BizCardX: Extracting Business Card Data with OCR",
                   layout="wide")

def setting_bg():
    st.markdown(f""" <style>.stApp {{
                        background:url("data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBw8PDw8PDw8VFRUPDw8PDxUPFQ8PDw8PFRUWFhUVFRUYHSggGBolHRUVITEhJSkrLi4uFx8zODMtNygtLisBCgoKDQ0NFQ8PFS0dHR0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLf/AABEIAKgBLAMBIgACEQEDEQH/xAAWAAEBAQAAAAAAAAAAAAAAAAAAAQf/xAAWEAEBAQAAAAAAAAAAAAAAAAAAARH/xAAXAQEBAQEAAAAAAAAAAAAAAAAAAQIF/8QAFREBAQAAAAAAAAAAAAAAAAAAAAH/2gAMAwEAAhEDEQA/AMYAdBhQFAFUQFAAURQAAAAAAAAAgAAAAAAAAACKAgCAAgGAAAAAoAAKYAAKAAAAAqACoACqIKgAqAAIAAAAFAABEAAAAABAAUAUABQAAAABVEUAEUBBQEBQEVAAEAAAAAABFEEAAMBAAAAUUEBQFAABUFFEUARQAAAAAAQUABAAAAEAAAABAQAAAEABQVAFAUAAFQUFQAUAAAAAAAEUBAqggAACAAACAqKIIAAAgAKAAKIqgAAAAoKAAAAAAAAAICoqAqAAAgAAgqIAAAAACAAoAAoCgAAAAAooigAAIqApQAAABAAAAEAEBUVEAAAAEAZFAUAFFEAVFFAAAAFQFFEUAEAVFBAAAEAAAABFRAAAAAAqCKggoiqAAACgqKAAoAAAAAAKgoAIAAAAAICiKCCogAAAIAAIAgKigAKAAACiiACxBRQQFAAEUAAAABFQBREAAAAABAAAEAAEUFBEUFABQAAAAFAAAEUAABFABFARQBAABQEAQAAEUKIAg//Z");
                        background-size: cover}}
                     </style>""", unsafe_allow_html=True)
setting_bg()

# Streamlit Title and Headers
st.markdown("<h1 style='text-align: center;font-size: 40px;'>BISCARDX: Extracting Business Card Data with OCR</h1>", 
            unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center;font-size: 25px;'>The Most Versatile Business Card Scanner</h1>", 
            unsafe_allow_html=True)

add_selectbox=option_menu(menu_title="Business Card Toolkit 📇",
                        options=["Fetch & Uncover Card", "Enhancements","Eradicate Card"],
                    icons=["archive","cloud-upload","database-add","search"],
                    default_index=0,
                    orientation="horizontal"
                    )

with st.sidebar:
    st.title("Avilable Business Cards")
    st.image("C:\\Users\\91822\\OneDrive\\Documents\\Capstone-03\\Capstone3\\Borcelle Airlines.png")
    
if add_selectbox == "Fetch & Uncover Card":
    mycursor.execute(
            "select Company_Name,Card_Holder_Name,Designation,Mobile_Number,Email_Id,Website,Street,District,State,Pincode from card_details1")
    updated_df = pd.DataFrame(mycursor.fetchall(),
                                columns=["Company_Name", "Card_Holder_Name", "Designation", "Mobile_Number",
                                        "Email_Id",
                                        "Website", "Street", "District", "State", "PinCode"])
    st.subheader(":blue[Upload a Business Card]")
    uploaded_card = st.file_uploader("upload here", label_visibility="collapsed", type=["png", "jpeg", "jpg"])
    #"C:\Users\91822\OneDrive\Documents\Capstone-03\Capstone3\3.png"

    if uploaded_card is not None:

        def save_card(uploaded_card):
            uploaded_cards_dir = os.path.join(os.getcwd(), "uploaded_cards")
            with open(os.path.join(uploaded_cards_dir), "wb") as f:
                f.write(uploaded_card.getbuffer())

        save_card(uploaded_card)

        def image_preview(image, res):
            for (bbox, text, prob) in res:
                # unpack the bounding box
                (tl, tr, br, bl) = bbox
                tl = (int(tl[0]), int(tl[1]))
                tr = (int(tr[0]), int(tr[1]))
                br = (int(br[0]), int(br[1]))
                bl = (int(bl[0]), int(bl[1]))
                cv2.rectangle(image, tl, br, (0, 255, 0), 2)
                cv2.putText(image, text, (tl[0], tl[1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
            plt.rcParams['figure.figsize'] = (15, 15)
            plt.axis('off')
            plt.imshow(image)

        # DISPLAYING THE UPLOADED CARD
        col1, col2 = st.columns(2, gap="large")
        with col1:
            st.markdown("#     ")
            st.markdown("#     ")
            st.markdown("### You have uploaded the card")
            st.image(uploaded_card)
        # DISPLAYING THE CARD WITH HIGHLIGHTS
        with col2:
            st.markdown("#     ")
            st.markdown("#     ")
            with st.spinner("Please wait processing image..."):
                st.set_option('deprecation.showPyplotGlobalUse', False)
                saved_img = os.getcwd() + "\\" + "uploaded_cards" 
                image = cv2.imread(saved_img)
                res = reader.readtext(saved_img)
                st.markdown("### Image Processed and Data Extracted")
                st.pyplot(image_preview(image, res))

                # easy OCR
        saved_img = os.getcwd() + "\\" + "uploaded_cards" 
        result = reader.readtext(saved_img, detail=0, paragraph=False)

         # CONVERTING IMAGE TO BINARY TO UPLOAD TO SQL DATABASE
        def img_to_binary(file):
            # Convert image data to binary format
            with open(file, 'rb') as file:
                binaryData = file.read()
            return binaryData
        data = {"Company_Name": [],
                "Card_Holder_Name": [],
                "Designation": [],
                "Mobile_Number": [],
                "Email_Id": [],
                "Website": [],
                "Street": [],
                "District": [],
                "State": [],
                "Pincode": []
                
                }
        
        def get_data(res):
            for ind, i in enumerate(res):

                # To get WEBSITE_URL
                if "www " in i.lower() or "www." in i.lower():
                    data["Website"].append(i)
                elif "WWW" in i:
                    data["Website"] = res[4] + "." + res[5]

                # To get EMAIL ID
                elif "@" in i:
                    data["Email_Id"].append(i)

                # To get MOBILE NUMBER
                elif "-" in i:
                    data["Mobile_Number"].append(i)
                    if len(data["Mobile_Number"]) == 2:
                        data["Mobile_Number"] = " & ".join(data["Mobile_Number"])

                # To get COMPANY NAME
                elif ind == len(res) - 1:
                    data["Company_Name"].append(i)

                # To get CARD HOLDER NAME
                elif ind == 0:
                    data["Card_Holder_Name"].append(i)

                # To get DESIGNATION
                elif ind == 1:
                    data["Designation"].append(i)

                # To get AREA
                if re.findall('^[0-9].+, [a-zA-Z]+', i):
                    data["Street"].append(i.split(',')[0])
                elif re.findall('[0-9] [a-zA-Z]+', i):
                    data["Street"].append(i)

                # To get CITY NAME
                match1 = re.findall('.+St , ([a-zA-Z]+).+', i)
                match2 = re.findall('.+St,, ([a-zA-Z]+).+', i)
                match3 = re.findall('^[E].*', i)
                if match1:
                    data["District"].append(match1[0])
                elif match2:
                    data["District"].append(match2[0])
                elif match3:
                    data["District"].append(match3[0])

                # To get STATE
                state_match = re.findall('[a-zA-Z]{9} +[0-9]', i)
                if state_match:
                    data["State"].append(i[:9])
                elif re.findall('^[0-9].+, ([a-zA-Z]+);', i):
                    data["State"].append(i.split()[-1])
                if len(data["State"]) == 2:
                    data["State"].pop(0)

                # To get PINCODE
                if len(i) >= 6 and i.isdigit():
                    data["Pincode"].append(i)
                elif re.findall('[a-zA-Z]{9} +[0-9]', i):
                    data["Pincode"].append(i[10:])


        get_data(result)

        # FUNCTION TO CREATE DATAFRAME
        def create_df(data):
            df = pd.DataFrame(data)
            return df


        df = create_df(data)
        st.success("### Data Extracted!")
        st.write(df)

        if st.button("Upload to Database"):
            for i, row in df.iterrows():
                # here %S means string values
                sql = """INSERT INTO card_details1(Company_Name,Card_Holder_Name,Designation,Mobile_Number,Email_Id,Website,Street,District,State,Pincode)
                         VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                mycursor.execute(sql, tuple(row))
                # the connection is not auto committed by default, so we must commit to save our changes
                mydb.commit()
                st.success("#### Uploaded to database successfully!")

        if st.button(":blue[View updated data]"):
            mycursor.execute("select Company_name,Card_Holder_Name,Designation,Mobile_Number,Email_Id,Website,Street,District,State,Pincode from card_details1")
            updated_df = pd.DataFrame(mycursor.fetchall(),
                                          columns=["Company_Name", "Card_Holder_Name", "Designation", "Mobile_Number",
                                                   "Email_Id",
                                                   "Website", "Street", "District", "State", "Pincode"])
            st.write(updated_df)

if add_selectbox == "Enhancements":
    st.subheader(':blue[You can view , alter or delete the extracted data in this app]')
    select = st.selectbox("Select an option:",
                               options=["ALTER", "DELETE"],
                               index=0,
                               format_func=lambda x: x.upper())
    if select == "ALTER":
        st.markdown(":blue[Alter the data here]")

        try:
            mycursor.execute("SELECT Card_Holder_Name FROM card_details1")
            result = mycursor.fetchall()
            business_cards = {}
            for row in result:
                business_cards[row[0]] = row[0]
            options = ["None"] + list(business_cards.keys())
            selected_card = st.selectbox("**Select a card**", options)
            if selected_card == "None":
                st.write("No card selected.")
            else:
                st.markdown("#### Update or modify any data below")
                mycursor.execute(
                "select Company_Name,Card_Holder_Name,Designation,Mobile_Number,Email_Id,Website,Street,District,State,Pincode from card_details1 WHERE Card_Holder_Name=%s",
                (selected_card,))
                result = mycursor.fetchone()

                # DISPLAYING ALL THE INFORMATIONS
                Company_Name = st.text_input("Company_Name", result[0])
                Card_Holder_Name = st.text_input("Card_Holder_Name", result[1])
                Designation = st.text_input("Designation", result[2])
                Mobile_Number = st.text_input("Mobile_Number", result[3])
                Email_Id = st.text_input("Email", result[4])
                Website = st.text_input("Website", result[5])
                Street = st.text_input("Street", result[6])
                District = st.text_input("District", result[7])
                State = st.text_input("State", result[8])
                Pincode = st.text_input("Pincode", result[9])

                if st.button(":blue[Commit changes to DB]"):

                   # Update the information for the selected business card in the database
                    mycursor.execute("""UPDATE card_details1 SET Company_Name=%s,Card_Holder_Name=%s,Designation=%s,Mobile_Number=%s,Email_Id=%s,Website=%s,Street=%s,District=%s,State=%s,Pincode=%s
                                    WHERE Card_Holder_Name=%s""", (Company_Name, Card_Holder_Name, Designation, Mobile_Number, Email_Id, Website, Street, District, State, Pincode,
                    selected_card))
                    mydb.commit()
                    st.success("Information updated in database successfully.")

            if st.button(":blue[View updated data]"):
                mycursor.execute(
                    "select Company_Name,Card_Holder_Name,Designation,Mobile_Number,Email_Id,Website,Street,District,State,Pincode from card_details1")
                updated_df = pd.DataFrame(mycursor.fetchall(),
                                          columns=["Company_Name", "Card_Holder_Name", "Designation", "Mobile_Number",
                                                   "Email",
                                                   "Website", "Street", "District", "State", "Pincode"])
                st.write(updated_df)

        except:
            st.warning("There is no data available in the database")

if add_selectbox == "Eradicate Card":
    st.subheader(":blue[Delete the data]")
    try:
        mycursor.execute("SELECT Card_Holder_Name FROM card_details1")
        result = mycursor.fetchall()
        business_cards = {}
        for row in result:
            business_cards[row[0]] = row[0]
        options = ["None"] + list(business_cards.keys())
        selected_card = st.selectbox("**Select a card**", options)
        if selected_card == "None":
            st.write("No card selected.")
        else:
            st.write(f"### You have selected :green[**{selected_card}'s**] card to delete")
            st.write("#### Proceed to delete this card?")
            if st.button("Yes Delete Business Card"):
                mycursor.execute(f"DELETE FROM card_details1 WHERE Card_Holder_Name='{selected_card}'")
                mydb.commit()
                st.success("Business card information deleted from database.")

        if st.button(":blue[View updated data]"):
            mycursor.execute(
                "select Company_Name,Card_Holder_Name,Designation,Mobile_Number,Email_Id,Website,Street,District,State,Pincode from card_details1")
            updated_df = pd.DataFrame(mycursor.fetchall(),
                                        columns=["Company_Name", "Card_Holder_Name", "Designation", "Mobile_Number",
                                                "Email",
                                                "Website", "Street", "District", "State", "Pincode"])
            st.write(updated_df)

    except:
        st.warning("There is no data available in the database")
