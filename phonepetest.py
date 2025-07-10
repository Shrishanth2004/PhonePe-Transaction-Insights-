import streamlit as st
from streamlit_option_menu import option_menu
import psycopg2
import pandas as pd
import plotly.express as px 
import json
import requests
from PIL import Image 


#DataFrame creation
#sql connection
mydb= psycopg2.connect(host="localhost",
                       user="postgres",
                       port="5432",
                       database="phonepe",
                       password="Shri@2004")
cursor=mydb.cursor()

#---------------------------------------------------------------------------
#agg_insurance_df
cursor.execute("SELECT * FROM aggregated_insurance")
mydb.commit()
table1=cursor.fetchall()

Aggre_insurance=pd.DataFrame(table1,columns=("State","Years","Quater","Transaction_type","Transaction_count","Transaction_amount"))


#agg_transaction_df
cursor.execute("SELECT * FROM aggregated_transaction")
mydb.commit()
table2=cursor.fetchall()

Aggre_transaction=pd.DataFrame(table2,columns=("State","Years","Quater","Transaction_type","Transaction_count","Transaction_amount"))


#agg_user_df
cursor.execute("SELECT * FROM aggregated_user")
mydb.commit()
table3=cursor.fetchall()

Aggre_user=pd.DataFrame(table3,columns=("State","Years","Quater","Brands","Transaction_count","Percentage"))

#--------------------------------------------------------------------------------------------------------------
#map_insurance_df
cursor.execute("SELECT * FROM map_insurance")
mydb.commit()
table4=cursor.fetchall()

Map_insurance=pd.DataFrame(table4,columns=("State","Years","Quater","District","Transaction_count","Transaction_amount"))


#map_transaction_df
cursor.execute("SELECT * FROM map_transaction")
mydb.commit()
table5=cursor.fetchall()

Map_transaction=pd.DataFrame(table5,columns=("State","Years","Quater","District","Transaction_count","Transaction_amount"))


#map_user_df
cursor.execute("SELECT * FROM map_user")
mydb.commit()
table6=cursor.fetchall()

Map_user=pd.DataFrame(table6,columns=("State","Years","Quater","District","RegisteredUserst","AppOpens"))

#------------------------------------------------------------------------------------------------------------

#top_insurance_df
cursor.execute("SELECT * FROM top_insurance")
mydb.commit()
table7=cursor.fetchall()

Top_insurance=pd.DataFrame(table7,columns=("State","Years","Quater","Pincodes","Transaction_count","Transaction_amount"))


#top_transaction_df
cursor.execute("SELECT * FROM top_transaction")
mydb.commit()
table8=cursor.fetchall()

Top_transaction=pd.DataFrame(table8,columns=("State","Years","Quater","Pincodes","Transaction_count","Transaction_amount"))


#top_user_df
cursor.execute("SELECT * FROM top_user")
mydb.commit()
table9=cursor.fetchall()

Top_user=pd.DataFrame(table9,columns=("State","Years","Quater","Pincodes","RegisteredUsers"))


#Transaction Year Based
def Transaction_amount_count_Y(df, year):
    tacy=df[df["Years"]==year]   
    tacy.reset_index(drop=True,inplace=True) 

    tacyg=tacy.groupby("State")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:
        fig_amount=px.bar(tacyg, x="State" ,y="Transaction_amount", title=f"{year} TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Bluered_r,height=650, width=600)

        st.plotly_chart(fig_amount)

    with col2:
        fig_count=px.bar(tacyg, x="State" ,y="Transaction_count", title=f"{year} TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Bluered,height=650, width=600)

        st.plotly_chart(fig_count)
    
    
    return tacy
    

def Transaction_amount_count_Y_Q(df, quarter):
    tacy=df[df["Quater"]==quarter]   
    tacy.reset_index(drop=True,inplace=True) 

    tacyg=tacy.groupby("State")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:
        
        fig_amount=px.bar(tacyg, x="State" ,y="Transaction_amount", title=f"{tacy['Years'].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Bluered_r,height=650, width=600)

        st.plotly_chart(fig_amount)

    with col2:
        
        fig_count=px.bar(tacyg, x="State" ,y="Transaction_count", title=f"{tacy['Years'].min()} YEAR {quarter} QUARTER TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Bluered,height=650, width=600)

        st.plotly_chart(fig_count)
        
    return tacy


def Aggre_Tran_Transaction_type(df, state):
    tacy=df[df["State"]==state]   
    tacy.reset_index(drop=True,inplace=True) 

    
    tacyg=tacy.groupby("Transaction_type")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)
    
    col1,col2=st.columns(2)
    with col1:
        
        fig_pie1=px.pie(data_frame= tacyg, names="Transaction_type", values="Transaction_amount",
                        width=600, title=f"{state.upper()} TRANSACTION AMOUNT",  hole=0.5)
        st.plotly_chart(fig_pie1)
        
    with col2:
        fig_pie2=px.pie(data_frame= tacyg, names="Transaction_type", values="Transaction_count",
                        width=600, title=f"{state.upper()} TRANSACTION COUNT",  hole=0.5)
        st.plotly_chart(fig_pie2)


#Aggregated user analysis1
def Aggre_user_plot1(df,year):
    aguy=df[df["Years"]==year]
    aguy.reset_index(drop=True,inplace= True)

    aguyg=pd.DataFrame(aguy.groupby("Brands")["Transaction_count"].sum())
    aguyg.reset_index(inplace=True)

    fig_bar1=px.bar(aguyg, x="Brands",y="Transaction_count", title=f"{year} BRANDS AND TRANSACTION COUNT",
                    width=1000, color_discrete_sequence=px.colors.sequential.Greens_r,hover_name="Brands")
    st.plotly_chart(fig_bar1)
    
    return aguy


# Aggregated user analysis 2
def Aggre_user_plot2(df, quarter):
    aguyq=df[df["Quater"]==quarter]
    aguyq.reset_index(drop=True,inplace= True)

    aguyqg=pd.DataFrame(aguyq.groupby("Brands")["Transaction_count"].sum())
    aguyqg.reset_index(inplace=True)

    fig_bar2=px.bar(aguyqg, x="Brands",y="Transaction_count", title=f"{quarter} QUARTER, BRANDS AND TRANSACTION COUNT",
                        width=1000, color_discrete_sequence=px.colors.sequential.Greens_r,hover_name="Brands")
    st.plotly_chart(fig_bar2)
    
    return aguyq


#aggregated user analysis 3
def Aggre_user_plot3(df,state):
    auyqs=df[df["State"]==state]
    auyqs.reset_index(drop=True,inplace=True)

    fig_line1=px.line(auyqs, x="Brands",y="Transaction_count", hover_data= "Percentage",
                    title=f"{state.upper()} BRANDS, TRANSACTION COUNT, PERCENTAGE",width=1000,markers=True)
    
    st.plotly_chart(fig_line1)
    
    
#map insurance district 
def Map_insur_District(df, state):
    
    tacy=df[df["State"]==state]   
    tacy.reset_index(drop=True,inplace=True) 

    tacyg=tacy.groupby("District")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)
    
    col1,col2=st.columns(2)
    with col1:
        fig_bar1=px.bar(tacyg, x="Transaction_amount", y="District", orientation="h", height=600,
                        title=f"{state.upper()} DISTRICT AND TRANSACTION AMOUNT",color_discrete_sequence= px.colors.sequential.Mint_r)
        st.plotly_chart(fig_bar1)
    with col2:
        fig_bar2=px.bar(tacyg, x="Transaction_count", y="District", orientation="h",height=600,
                        title=f"{state.upper()} DISTRICT AND TRANSACTION COUNT",color_discrete_sequence= px.colors.sequential.Redor_r)
        st.plotly_chart(fig_bar2)


#map user plot1
def map_user_plot1(df,year):
    muy=df[df["Years"]==year]
    muy.reset_index(drop=True,inplace= True)

    muyg=pd.DataFrame(muy.groupby("State")[["RegisteredUserst", "AppOpens"]].sum())
    muyg.reset_index(inplace=True)
    

    fig_line1=px.line(muy, x="State",y=["RegisteredUserst", "AppOpens"],
                        title=f"{year} REGISTERED USER, APPOPENS",width=1000,height=800,markers=True)
    st.plotly_chart(fig_line1)
    
    return muy


#map user plot2
def map_user_plot2(df,quarter):
    muyq=df[df["Quater"]==quarter]
    muyq.reset_index(drop=True,inplace= True)

    muyqg=pd.DataFrame(muyq.groupby("State")[["RegisteredUserst", "AppOpens"]].sum())
    muyqg.reset_index(inplace=True)
    

    fig_line2=px.line(muyqg, x="State",y=["RegisteredUserst", "AppOpens"],
                        title=f"{df['Years'].min()} YEARS {quarter} QUARTER REGISTERED USER, APPOPENS",width=1000,height=800,markers=True)
    st.plotly_chart(fig_line2)
    
    return muyq


#map user plot3
def map_user_plot3(df,state):
    muyqs=df[df["State"]==state]
    muyqs.reset_index(drop=True,inplace= True)
    col1,col2=st.columns(2)
    with col1:
        fig_map_user_bar1=px.bar(muyqs, x="RegisteredUserst", y="District", orientation="h",
                                title=f"{state.upper()} REGISTERED USER", height=700, color_discrete_sequence=px.colors.sequential.RdBu_r)
        st.plotly_chart(fig_map_user_bar1)
    with col2:
        fig_map_user_bar2=px.bar(muyqs, x="AppOpens", y="District", orientation="h",
                                title=f"{state.upper()} APP OPENS", height=700, color_discrete_sequence=px.colors.sequential.Bluered_r)
        st.plotly_chart(fig_map_user_bar2)
    

#top insurance plot1
def Top_insurance_plot1(df,state):
    tiy=df[df["State"]==state]
    tiy.reset_index(drop=True,inplace= True)

    col1,col2=st.columns(2)
    with col1:
        fig_top_insur_bar1=px.bar(tiy, x="Quater", y="Transaction_amount", hover_data="Pincodes",
                                    title= "TRANSACTION AMOUNT", height=700, color_discrete_sequence=px.colors.sequential.BuGn_r)
        st.plotly_chart(fig_top_insur_bar1)
        
    with col2: 
        fig_top_insur_bar2=px.bar(tiy, x="Quater", y="Transaction_count",hover_data="Pincodes",
                                    title= "TRANSACTION COUNT", height=700, color_discrete_sequence=px.colors.sequential.Blues_r)
        st.plotly_chart(fig_top_insur_bar2)
        
        
        
#top user plot 1
def Top_user_plot1(df,year):
    tuy=df[df["Years"]==year]
    tuy.reset_index(drop=True,inplace= True)

    tuyg=pd.DataFrame(tuy.groupby(["State","Quater"])["RegisteredUsers"].sum())
    tuyg.reset_index(inplace=True)

    fig_top_plot1=px.bar(tuyg, x="State", y="RegisteredUsers",color="Quater",width=1000,height=800,hover_name="State",
                        color_discrete_sequence=px.colors.sequential.Burgyl,title=f"{year} REGISTERED USER")
    st.plotly_chart(fig_top_plot1)
    
    return tuy


#top user plot 2
def Top_user_plot2(df,state):
    tuys=df[df["State"]==state]
    tuys.reset_index(drop=True,inplace= True)

    fig_top_plot2=px.bar(tuys, x="Quater",y="RegisteredUsers", title=f"{state.upper()} REGISTRED USER, PINCODDES, QUARTERS",
                        width=1000,height=800,color="RegisteredUsers", hover_data="Pincodes",color_continuous_scale=px.colors.sequential.Magenta_r)
    st.plotly_chart(fig_top_plot2)


#sql connection
def top_chart_transaction_amount(table_name):
        mydb= psycopg2.connect(host="localhost",
                        user="postgres",
                        port="5432",
                        database="phonepe",
                        password="Shri@2004")
        cursor=mydb.cursor()

        #plot1 
        query1=f'''SELECT state, sum(transaction_amount) as transaction_amount
                FROM {table_name}
                group by state
                order by transaction_amount desc
                limit 10;'''
        cursor.execute(query1)
        table1=cursor.fetchall()
        mydb.commit()

        df1=pd.DataFrame(table1, columns=("state","transaction_amount"))
        
        col1,col2=st.columns(2)
        with col1:
            fig_amount=px.bar(df1, x="state" ,y="transaction_amount", title=" TOP 10 OF TRANSACTION AMOUNT",
                            color_discrete_sequence=px.colors.sequential.Bluered_r,height=650, width=600,hover_name="state")

            st.plotly_chart(fig_amount)

        #plot2
        query2=f'''SELECT state, sum(transaction_amount) as transaction_amount
                FROM {table_name}
                group by state
                order by transaction_amount 
                limit 10;'''
        cursor.execute(query2)
        table2=cursor.fetchall()
        mydb.commit()

        df2=pd.DataFrame(table2, columns=("state","transaction_amount"))
        with col2:
            fig_amount2=px.bar(df2, x="state" ,y="transaction_amount", title="LAST 10 OF TRANSACTION AMOUNT",
                            color_discrete_sequence=px.colors.sequential.Blues_r,height=650, width=600,hover_name="state")

            st.plotly_chart(fig_amount2)


        #plot3
        query3=f'''SELECT state, avg(transaction_amount) as transaction_amount
                FROM {table_name}
                group by state
                order by transaction_amount ;'''
        cursor.execute(query3)
        table3=cursor.fetchall()
        mydb.commit()

        df3=pd.DataFrame(table3, columns=("state","transaction_amount"))
        fig_amount3=px.bar(df3, y="state" ,x="transaction_amount", title="AVERAGE OF TRANSACTION AMOUNT", orientation="h",
                        color_discrete_sequence=px.colors.sequential.Bluered,height=800, width=1000,hover_name="state")

        st.plotly_chart(fig_amount3)
        
        
#sql connection
def top_chart_transaction_count(table_name):
        mydb= psycopg2.connect(host="localhost",
                        user="postgres",
                        port="5432",
                        database="phonepe",
                        password="Shri@2004")
        cursor=mydb.cursor()

        #plot1 
        query1=f'''SELECT state, sum(transaction_count) as transaction_count
                FROM {table_name}
                group by state
                order by transaction_count desc
                limit 10;'''
        cursor.execute(query1)
        table1=cursor.fetchall()
        mydb.commit()

        df1=pd.DataFrame(table1, columns=("state","transaction_count"))
        
        col1,col2=st.columns(2)
        with col1:
            fig_amount=px.bar(df1, x="state" ,y="transaction_count", title="TOP 10 OF TRANSACTION COUNT",
                            color_discrete_sequence=px.colors.sequential.Bluered_r,height=650, width=600,hover_name="state")

            st.plotly_chart(fig_amount)

        #plot2
        query2=f'''SELECT state, sum(transaction_count) as transaction_count
                FROM {table_name}
                group by state
                order by transaction_count 
                limit 10;'''
        cursor.execute(query2)
        table2=cursor.fetchall()
        mydb.commit()

        df2=pd.DataFrame(table2, columns=("state","transaction_count"))
        with col2:
            fig_amount2=px.bar(df2, x="state" ,y="transaction_count", title="LAST 10 OF TRANSACTION COUNT",
                            color_discrete_sequence=px.colors.sequential.Blues_r,height=650, width=600,hover_name="state")

            st.plotly_chart(fig_amount2)


        #plot3
        query3=f'''SELECT state, avg(transaction_count) as transaction_count
                FROM {table_name}
                group by state
                order by transaction_count ;'''
        cursor.execute(query3)
        table3=cursor.fetchall()
        mydb.commit()

        df3=pd.DataFrame(table3, columns=("state","transaction_count"))
        fig_amount3=px.bar(df3, y="state" ,x="transaction_count", title="AVERAGE OF TRANSACTION COUNT", orientation="h",
                        color_discrete_sequence=px.colors.sequential.Bluered,height=800, width=1000,hover_name="state")

        st.plotly_chart(fig_amount3)


#sql connection
def top_chart_registereduser(table_name, state):
        mydb= psycopg2.connect(host="localhost",
                        user="postgres",
                        port="5432",
                        database="phonepe",
                        password="Shri@2004")
        cursor=mydb.cursor()

        #plot1 
        query1=f'''select district, sum(registereduserst) as registereduser
                    from {table_name}
                    where state= '{state}'
                    group by district
                    order by registereduser desc
                    limit 10;'''
                    
        cursor.execute(query1)
        table1=cursor.fetchall()
        mydb.commit()

        df1=pd.DataFrame(table1, columns=("district","registereduser"))
        
        col1,col2=st.columns(2)
        with col1:
            fig_amount=px.bar(df1, x="district" ,y="registereduser", title="TOP 10 REGISTERED USER",
                            color_discrete_sequence=px.colors.sequential.Bluered_r,height=650, width=600,hover_name="district")

            st.plotly_chart(fig_amount)

        #plot2
        query2=f'''select district, sum(registereduserst) as registereduser
                    from {table_name}
                    where state= '{state}'
                    group by district
                    order by registereduser
                    limit 10;'''
                    
        cursor.execute(query2)
        table2=cursor.fetchall()
        mydb.commit()

        df2=pd.DataFrame(table1, columns=("district","registereduser"))
        
        with col2:
            fig_amount2=px.bar(df2, x="district" ,y="registereduser", title="LAST 10 REGISTERED USER",
                            color_discrete_sequence=px.colors.sequential.Blues_r,height=650, width=600,hover_name="district")

            st.plotly_chart(fig_amount2)


        #plot3
        query3=f'''select district, avg(registereduserst) as registereduser
                    from {table_name}
                    where state= '{state}'
                    group by district
                    order by registereduser;'''
                    
        cursor.execute(query3)
        table3=cursor.fetchall()
        mydb.commit()

        df3=pd.DataFrame(table3, columns=("district","registereduser"))
        
        fig_amount3=px.bar(df3, y="district" ,x="registereduser", title="AVERAGE OF REGISTERED USER",orientation="h",
                        color_discrete_sequence=px.colors.sequential.Bluered,height=800, width=1000,hover_name="district")

        st.plotly_chart(fig_amount3)
        
        
#sql connection
def top_chart_appopens(table_name, state):
        mydb= psycopg2.connect(host="localhost",
                        user="postgres",
                        port="5432",
                        database="phonepe",
                        password="Shri@2004")
        cursor=mydb.cursor()

        #plot1 
        query1=f'''select district, sum(appopens) as appopens
                    from {table_name}
                    where state= '{state}'
                    group by district
                    order by appopens desc
                    limit 10;'''
                    
        cursor.execute(query1)
        table1=cursor.fetchall()
        mydb.commit()

        df1=pd.DataFrame(table1, columns=("district","appopens"))
        
        col1,col2=st.columns(2)
        with col1:
            fig_amount=px.bar(df1, x="district" ,y="appopens", title="TOP 10 APPOPENS",
                            color_discrete_sequence=px.colors.sequential.Bluered_r,height=650, width=600,hover_name="district")

            st.plotly_chart(fig_amount)

        #plot2
        query2=f'''select district, sum(appopens) as appopens
                    from {table_name}
                    where state= '{state}'
                    group by district
                    order by appopens
                    limit 10;'''
                    
        cursor.execute(query2)
        table2=cursor.fetchall()
        mydb.commit()

        df2=pd.DataFrame(table1, columns=("district","appopens"))
        with col2:
            fig_amount2=px.bar(df2, x="district" ,y="appopens", title="LAST 10 APPOPENS",
                            color_discrete_sequence=px.colors.sequential.Bluered_r,height=650, width=600,hover_name="district")

            st.plotly_chart(fig_amount2)


        #plot3
        query3=f'''select district, avg(appopens) as appopens
                    from {table_name}
                    where state= '{state}'
                    group by district
                    order by appopens;'''
                    
        cursor.execute(query3)
        table3=cursor.fetchall()
        mydb.commit()

        df3=pd.DataFrame(table3, columns=("district","appopens"))
        
        fig_amount3=px.bar(df3, y="district" ,x="appopens", title="AVERAGE OF APPOPENS",orientation="h",
                        color_discrete_sequence=px.colors.sequential.Blues_r,height=650, width=600,hover_name="district")

        st.plotly_chart(fig_amount3)


#sql connection
def top_chart_registeredusers(table_name):
        mydb= psycopg2.connect(host="localhost",
                        user="postgres",
                        port="5432",
                        database="phonepe",
                        password="Shri@2004")
        cursor=mydb.cursor()

        #plot1 
        query1=f'''select state, sum(registeredusers) as registeredusers
                    from {table_name}
                    group by state
                    order by registeredusers desc
                    limit 10;'''
                    
        cursor.execute(query1)
        table1=cursor.fetchall()
        mydb.commit()

        df1=pd.DataFrame(table1, columns=("state","registeredusers"))
        
        col1,col2=st.columns(2)
        with col1:
            fig_amount=px.bar(df1, x="state" ,y="registeredusers", title="TOP 10 REGISTERED USER",
                            color_discrete_sequence=px.colors.sequential.Bluered,height=650, width=600,hover_name="state")

            st.plotly_chart(fig_amount)

        #plot2
        query2=f'''select state, sum(registeredusers) as registeredusers
                    from {table_name}
                    group by state
                    order by registeredusers
                    limit 10;'''
                    
        cursor.execute(query2)
        table2=cursor.fetchall()
        mydb.commit()

        df2=pd.DataFrame(table1, columns=("state","registeredusers"))
        
        with col2:
            fig_amount2=px.bar(df2, x="state" ,y="registeredusers", title="LAST 10 REGISTERED USER",
                            color_discrete_sequence=px.colors.sequential.Blues_r,height=650, width=600,hover_name="state")

            st.plotly_chart(fig_amount2)


        #plot3
        query3=f'''select state, avg(registeredusers) as registeredusers
                    from {table_name}
                    group by state
                    order by registeredusers;'''
                    
        cursor.execute(query3)
        table3=cursor.fetchall()
        mydb.commit()

        df3=pd.DataFrame(table3, columns=("state","registeredusers"))
        
        fig_amount3=px.bar(df3, y="state" ,x="registeredusers", title="AVERAGE OF REGISTERED USER",orientation="h",
                        color_discrete_sequence=px.colors.sequential.Bluered,height=650, width=600,hover_name="state")

        st.plotly_chart(fig_amount3)


    
#streamlit part

st.set_page_config(layout="wide")
st.title("PhonePe Data Visulization")

with st.sidebar:

    select=option_menu("Main Menu",["Home", "Data Exploration", "Top Charts", ])
    
if select == "Home":

    coll,col2= st.columns(2)
    with coll:
        st.header("PHONEPE")
        st.subheader("INDIA'S BEST TRANSACTION APP")
        st.markdown("PhonePe is an Indian digital payments and financial technology company")
        st.write("****FEATURES****")
        st.write("****Credit & Debit card linking****")
        st.write("****Bank Balance check****")
        st.write("****Money Storage****")
        st.write("****PIN Authorization****")
        st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")


    with col2:
        st.image(Image.open(r"C:\Users\Shrishanth S Shetty\OneDrive\Documents\Phonepe new\image1.jpeg"),width=600)


    col3,col4= st.columns(2)
    with col3:

        st.image(Image.open(r"C:\Users\Shrishanth S Shetty\OneDrive\Documents\Phonepe new\image2.jpeg"),width=600)
    with col4:
        st.write("****Easy Transactions****")
        st.write("****One App For All Your Payments****")
        st.write("****Your Bank Account Is All You Need****")
        st.write("****Multiple Payment Modes****")
        st.write("****PhonePe Merchants****")
        st.write("****Multiple Ways To Pay****")
        st.write("****1.Direct Transfer & More****")
        st.write("****2.QR Code****")
        st.write("****Earn Great Rewards****")
    
    col5, col6= st.columns(2)

    with col5:

        st.markdown(" ")
        st.markdown("")
        st.markdown("")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown("")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.write("****No Wallet Top-Up Required****")
        st.write("****Pay Directly From Any Bank To Any Bank A/C****")
        st.write("****Instantly & Free****")

    with col6:
        st.image(Image.open(r"C:\Users\Shrishanth S Shetty\OneDrive\Documents\Phonepe new\image3.jpeg"),width=600)
        


    
elif select=="Data Exploration":
    
    tab1,tab2,tab3=st.tabs(["Aggregated Analysis", "Map Analysis","Top Analysis"])
    
    with tab1:
        
        method=st.radio("Select The Method",["Insurance Analysis","Transaction Analysis","User Analysis"])
        
        if method== "Insurance Analysis":
            
            col1,col2=st.columns(2)
            with col1:
                
                years=st.slider("Select The Year",Aggre_insurance["Years"].min(),Aggre_insurance["Years"].max(),Aggre_insurance["Years"].min())
            tac_Y=Transaction_amount_count_Y(Aggre_insurance, years)
            
            col1,col2=st.columns(2)
            with col1:
                
                quarters=st.slider("Select The Quarter",tac_Y["Quater"].min(),tac_Y["Quater"].max(),tac_Y["Quater"].min())
            Transaction_amount_count_Y_Q(tac_Y,quarters)
                
        
        elif method == "Transaction Analysis":
            
            col1,col2=st.columns(2)
            with col1:
                
                years=st.slider("Select The Year",Aggre_transaction["Years"].min(),Aggre_transaction["Years"].max(),Aggre_transaction["Years"].min())
            Agg_tran_tac_Y=Transaction_amount_count_Y(Aggre_transaction, years)
            
            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select The State", Agg_tran_tac_Y["State"].unique())
                
            Aggre_Tran_Transaction_type(Agg_tran_tac_Y, states)
            
            col1,col2=st.columns(2)
            with col1:
                
                quarters=st.slider("Select The Quarter",Agg_tran_tac_Y["Quater"].min(),Agg_tran_tac_Y["Quater"].max(),Agg_tran_tac_Y["Quater"].min())
            Aggre_tran_tac_Y_Q= Transaction_amount_count_Y_Q(Agg_tran_tac_Y, quarters)
            
            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select The State_ty", Aggre_tran_tac_Y_Q["State"].unique())
                
            Aggre_Tran_Transaction_type(Aggre_tran_tac_Y_Q, states)
        
        elif method == "User Analysis":
            
            col1,col2=st.columns(2)
            with col1:
                
                years=st.slider("Select The Year",Aggre_user["Years"].min(),Aggre_user["Years"].max(),Aggre_user["Years"].min())
            Aggre_user_Y=Aggre_user_plot1(Aggre_user, years)
            
            col1,col2=st.columns(2)
            with col1:
                
                quarters=st.slider("Select The Quarter",Aggre_user_Y["Quater"].min(),Aggre_user_Y["Quater"].max(),Aggre_user_Y["Quater"].min())
            Aggre_user_Y_Q= Aggre_user_plot2(Aggre_user_Y, quarters)
            
            
            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select The State", Aggre_user_Y_Q["State"].unique())
                
            Aggre_user_plot3(Aggre_user_Y_Q, states)
            
            
 #-----------------------------------------------------------------------------------------------------------------------------------------------------------------------   
    
        
        
    with tab2:
        
        method2=st.radio("Select The Method",["Map Insurance", "Map Transaction", "Map User"])
        
        if method2== "Map Insurance":
            
            col1,col2=st.columns(2)
            with col1:
                
                years=st.slider("Select The Year_mi",Map_insurance["Years"].min(),Map_insurance["Years"].max(),Map_insurance["Years"].min())
            map_insur_tac_Y=Transaction_amount_count_Y(Map_insurance, years)
            
            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select The State_mi", map_insur_tac_Y["State"].unique())
                
            Map_insur_District(map_insur_tac_Y, states)
            
            col1,col2=st.columns(2)
            with col1:
                
                quarters=st.slider("Select The Quarter_mi",map_insur_tac_Y["Quater"].min(),map_insur_tac_Y["Quater"].max(),map_insur_tac_Y["Quater"].min())
            map_insur_tac_Y_Q= Transaction_amount_count_Y_Q(map_insur_tac_Y, quarters)
            
            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select The State_ty", map_insur_tac_Y_Q["State"].unique())
                
            Map_insur_District(map_insur_tac_Y_Q, states)
            
        elif method2 == "Map Transaction":
            col1,col2=st.columns(2)
            with col1:
                
                years=st.slider("Select The Year_mt",Map_transaction["Years"].min(),Map_transaction["Years"].max(),Map_transaction["Years"].min())
            map_tran_tac_Y=Transaction_amount_count_Y(Map_transaction, years)
            
            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select The State_mt", map_tran_tac_Y["State"].unique())
                
            Map_insur_District(map_tran_tac_Y, states)
            
            col1,col2=st.columns(2)
            with col1:
                
                quarters=st.slider("Select The Quarter_mt",map_tran_tac_Y["Quater"].min(),map_tran_tac_Y["Quater"].max(),map_tran_tac_Y["Quater"].min())
            map_tran_tac_Y_Q= Transaction_amount_count_Y_Q(map_tran_tac_Y, quarters)
            
            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select The State_mty", map_tran_tac_Y_Q["State"].unique())
                
            Map_insur_District(map_tran_tac_Y_Q, states)
        
        elif method2 == "Map User":
            col1,col2=st.columns(2)
            with col1:
                
                years=st.slider("Select The Yea_mu",Map_user["Years"].min(),Map_user["Years"].max(),Map_user["Years"].min())
            map_user_tac_Y=map_user_plot1(Map_user, years)
    
            col1,col2=st.columns(2)
            with col1:
                
                quarters=st.slider("Select The Quarter_mu",map_user_tac_Y["Quater"].min(),map_user_tac_Y["Quater"].max(),map_user_tac_Y["Quater"].min())
            Map_user_Y_Q= map_user_plot2(map_user_tac_Y, quarters)
            
    
            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select The State_mu", Map_user_Y_Q["State"].unique())
                
            map_user_plot3(Map_user_Y_Q, states)
    
    
 #-----------------------------------------------------------------------------------------------------------------------------------------------------------------------   
        
    with tab3:
        
        method3=st.radio("Select The Method",["Top Insurance", "Top Transaction", "Top User"])
        
        if method3== "Top Insurance":
           
            col1,col2=st.columns(2)
            with col1:
                
                years=st.slider("Select The Year_ti",Top_insurance["Years"].min(),Top_insurance["Years"].max(),Top_insurance["Years"].min())
            top_insur_tac_Y=Transaction_amount_count_Y(Top_insurance, years)
                
            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select The State_ti", top_insur_tac_Y["State"].unique())
                
            Top_insurance_plot1(top_insur_tac_Y, states)
            
            col1,col2=st.columns(2)
            with col1:
                
                quarters=st.slider("Select The Quarter_ti",top_insur_tac_Y["Quater"].min(),top_insur_tac_Y["Quater"].max(),top_insur_tac_Y["Quater"].min())
            Top_insur_tac_Y_Q= Transaction_amount_count_Y_Q(top_insur_tac_Y, quarters)
            
            
        
        elif method3 == "Top Transaction":
            
            col1,col2=st.columns(2)
            with col1:
                
                years=st.slider("Select The Year_tt",Top_transaction["Years"].min(),Top_transaction["Years"].max(),Top_transaction["Years"].min())
            top_tran_tac_Y=Transaction_amount_count_Y(Top_transaction, years)
                
            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select The State_tt", top_tran_tac_Y["State"].unique())
                
            Top_insurance_plot1(top_tran_tac_Y, states)
            
            col1,col2=st.columns(2)
            with col1:
                
                quarters=st.slider("Select The Quarter_tt",top_tran_tac_Y["Quater"].min(),top_tran_tac_Y["Quater"].max(),top_tran_tac_Y["Quater"].min())
            Top_tran_tac_Y_Q= Transaction_amount_count_Y_Q(top_tran_tac_Y, quarters)
        
        elif method3 == "Top User":
            
            col1,col2=st.columns(2)
            with col1:
                
                years=st.slider("Select The Year_tu",Top_user["Years"].min(),Top_user["Years"].max(),Top_user["Years"].min())
            top_user_Y=Top_user_plot1(Top_user, years)
            
            
            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select The State_tu", top_user_Y["State"].unique())
                
            Top_user_plot2(top_user_Y, states)
            
            
 #-----------------------------------------------------------------------------------------------------------------------------------------------------------------------   

        
elif select=="Top Charts":
    question=st.selectbox("Select the Question",["1. Transaction Amount and Count of Aggregated Insurance",

                                                "2. Transaction Amount and Count of Map Insurance",

                                                "3. Transaction Amount and Count of Top Insurance",

                                                "4. Transaction Amount and Count of Aggregated Transaction",

                                                "5. Transaction Amount and Count of Map Transaction",

                                                "6. Transaction Amount and Count of Top Transaction",

                                                "7. Transaction Count of Aggregated User",

                                                "8. Registered users of Map User",

                                                "9. App opens of Map User",

                                                "10. Registered users of Top User"])
    
    
    
    if question=="1. Transaction Amount and Count of Aggregated Insurance":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("aggregated_insurance")
        
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_insurance")
        
        
    elif question=="2. Transaction Amount and Count of Map Insurance":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("map_insurance")
        
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("map_insurance")
        
        
    elif question=="3. Transaction Amount and Count of Top Insurance":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("top_insurance")
        
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("top_insurance")
        
        
    elif question=="4. Transaction Amount and Count of Aggregated Transaction":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("aggregated_transaction")
        
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_transaction")
        
        
    elif question=="5. Transaction Amount and Count of Map Transaction":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("map_transaction")
        
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("map_transaction")
        
        
    elif question=="6. Transaction Amount and Count of Top Transaction":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("top_transaction")
        
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("top_transaction")    
    
    
    elif question=="7. Transaction Count of Aggregated User":
         
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_user")
        
        
    elif question=="8. Registered users of Map User":
        
        states= st.selectbox("Select The State",Map_user["State"].unique())
        st.subheader("REGISTERED USER")
        top_chart_registereduser("map_user",states)
        
        
    elif question=="9. App opens of Map User":
        
        states= st.selectbox("Select The State",Map_user["State"].unique())
        st.subheader("APPOPENS")
        top_chart_appopens("map_user",states)
        
        
    elif question=="10. Registered users of Top User":
         
        st.subheader("REGISTERED USERS")
        top_chart_registeredusers("top_user")

        