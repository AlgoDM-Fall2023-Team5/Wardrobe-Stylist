import pandas as pd
#import streamlit as st
from sqlalchemy import create_engine, MetaData, Table, select


snowflake_url = "snowflake://shirish:Northeastern123@PXTNTMC-FTB58373/CLOTHING_TAGS/PUBLIC?warehouse=COMPUTE_WH&role=ACCOUNTADMIN"

def annotations_list(snowflake_url):
    # Create an SQLAlchemy engine
    engine = create_engine(snowflake_url)

    try:
        with engine.connect() as conn:
            sql_query = "select annotations from wardrobe_tags;"
            
            result2 = conn.execute(sql_query)

            annotations_data = pd.DataFrame(result2.fetchall(), columns=result2.keys())
            annotations_data = annotations_data['annotations'].tolist()

            
    except Exception as e:
            print(e)
    finally:
        # Close the connection
        conn.close()

    return annotations_data

if __name__ == "__main__":
     
     annotations_list(snowflake_url)