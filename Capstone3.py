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

create_table_query="""CREATE TABLE IF NOT EXISTS card_details(
                        Company_Name varchar(30),
                        Card_Holder_Name varchar(30) Primary Key,
                        Designation varchar(30),
                        Mobile_Number Varchar(255),
                        Email_Id varchar(255) UNIQUE,
                        Website varchar(100),
                        Street varchar(50),
                        District varchar(50),
                        State varchar(30),
                        Pincode varchar(10)
                        )"""
mycursor.execute(create_table_query)
mydb.commit()


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
                    icons=["person-vcard-fill","postcard-fill","trash3-fill"],
                    default_index=0,
                    orientation="horizontal"
                    )

with st.sidebar:
    st.title(":purple[An Introductory Overview]")
    st.image("data:image/jpeg;base64,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")
    st.header(":blue[1.Scanning the Card:]")
    st.write("Initiating the Data Capture Process")
    st.header(":blue[2.Processing the Card:]")
    st.write("Transforming Captured Data into Usable Information")
    st.header(":blue[3.Storing the Data in the Database:]")
    st.write("Securing Information for Future Access and Analysis")
    st.header(":blue[4.Making Changes or Deleting the Card:]")
    st.write("Managing Data Integrity and User Control")
    
if add_selectbox == "Fetch & Uncover Card":
    mycursor.execute(
            "select Company_Name,Card_Holder_Name,Designation,Mobile_Number,Email_Id,Website,Street,District,State,Pincode from card_details")
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
            st.markdown("### Uploaded Card")
            st.image(uploaded_card)
        # DISPLAYING THE CARD WITH HIGHLIGHTS
        with col2:
            st.markdown("#     ")            
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
                        data["Mobile_Number"] = " , ".join(data["Mobile_Number"])
                

                # To get COMPANY NAME
                elif ind == len(res) - 1:
                    data["Company_Name"].append(i)

                # To get CARD HOLDER NAME
                elif ind == 0:
                    data["Card_Holder_Name"].append(i)

                # To get DESIGNATION
                elif ind == 1:
                    data["Designation"].append(i)

                # To get Street
                if re.findall('^[0-9].+, [a-zA-Z]+', i):
                    data["Street"].append(i.split(',')[0])
                elif re.findall('[0-9] [a-zA-Z]+', i):
                    data["Street"].append(i)

                # To get District NAME
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
        col1,col2,col3=st.columns(3)
        with col1:
            a=st.button("Extract Data")
        with col2:
            b=st.button("Upload to Database")
        with col3:
            c=st.button(":blue[View updated data]")
        df = create_df(data)
        df.index=df.index+1
        
        if a:
            st.write(df)
       
        if b:
            for i, row in df.iterrows():
                # here %S means string values
                sql = """INSERT INTO card_details(Company_Name,Card_Holder_Name,Designation,Mobile_Number,Email_Id,Website,Street,District,State,Pincode)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                mycursor.execute(sql, tuple(row))
                # the connection is not auto committed by default, so we must commit to save our changes
                mydb.commit()
                st.success("Uploaded to database successfully!")
        
        if c:
            mycursor.execute("select Company_name,Card_Holder_Name,Designation,Mobile_Number,Email_Id,Website,Street,District,State,Pincode from card_details")
            updated_df = pd.DataFrame(mycursor.fetchall(),
                                        columns=["Company_Name", "Card_Holder_Name", "Designation", "Mobile_Number",
                                                "Email_Id",
                                                "Website", "Street", "District", "State", "Pincode"])
            st.write(updated_df)

if add_selectbox == "Enhancements":
    st.subheader(':blue[Modify Extracted Data: Easily Edit Information Within This App]')
    
    try:
        mycursor.execute("SELECT Card_Holder_Name FROM card_details")
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
            "select Company_Name,Card_Holder_Name,Designation,Mobile_Number,Email_Id,Website,Street,District,State,Pincode from card_details WHERE Card_Holder_Name=%s",
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
                mycursor.execute("""UPDATE card_details SET Company_Name=%s,Card_Holder_Name=%s,Designation=%s,Mobile_Number=%s,Email_Id=%s,Website=%s,Street=%s,District=%s,State=%s,Pincode=%s
                                WHERE Card_Holder_Name=%s""", (Company_Name, Card_Holder_Name, Designation, Mobile_Number, Email_Id, Website, Street, District, State, Pincode,
                selected_card))
                mydb.commit()
                st.success("Information Has Been Successfully Updated")

        if st.button(":blue[View updated data]"):
            mycursor.execute(
                "select Company_Name,Card_Holder_Name,Designation,Mobile_Number,Email_Id,Website,Street,District,State,Pincode from card_details")
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
        mycursor.execute("SELECT Card_Holder_Name FROM card_details")
        result = mycursor.fetchall()
        business_cards = {}
        for row in result:
            business_cards[row[0]] = row[0]
        options = ["None"] + list(business_cards.keys())
        selected_card = st.selectbox("**Select a card**", options)
        
        if selected_card == "None":
            st.write("No card selected.")
        else:
            st.write("#### Proceed to delete this card?")
            if st.button("Delete"):
                mycursor.execute(f"DELETE FROM card_details WHERE Card_Holder_Name='{selected_card}'")
                mydb.commit()
                st.success(" The selected card has been removed from the database.")

        if st.button(":blue[View updated data]"):
            mycursor.execute(
                "select Company_Name,Card_Holder_Name,Designation,Mobile_Number,Email_Id,Website,Street,District,State,Pincode from card_details")
            updated_df = pd.DataFrame(mycursor.fetchall(),
                                        columns=["Company_Name", "Card_Holder_Name", "Designation", "Mobile_Number",
                                                "Email",
                                                "Website", "Street", "District", "State", "Pincode"])
            st.write(updated_df)

    except:
        st.warning("There is no data available in the database")

        
