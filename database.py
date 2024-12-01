import psycopg2
from config import host, user, password, db_name

def create_db():
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )

        cursor = connection.cursor()
        cursor.execute(
                """CREATE TABLE Information_from_marketplaces(
                    Id serial PRIMARY KEY,
                    Article int,
                    Marketplace nchar(50),
                    CardName nchar(500),
                    Url nchar(1000),
                    Card_Price_With_Discount nchar(50),
                    Card_Price_Without_Discount nchar(50),
                    Description nchar(4000),
                    Quantity_Of_Goods nchar(50))
                    """
            )
        connection.commit()
        print("Table Created successfully")

    except Exception as _ex:
        print("Error while working with database", _ex)

    finally:
        if connection:
            connection.close()



def insert_into_database(marketplace, product_url, product_article, 
                        product_name, card_price_without_discount, 
                        card_price_with_discount, quantity_of_goods,
                        product_description):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )

        cursor = connection.cursor()
        cursor.execute(
            f"""INSERT INTO Information_from_Marketplaces
            (
                Article,
                Marketplace,
                CardName,
                Url,
                Card_Price_With_Discount,
                Card_Price_Without_Discount,
                Description,
                Quantity_Of_Goods
                
            ) 
            VALUES
            (
                %s, %s, %s, %s, %s, %s, %s, %s
            )
            """,
            (product_article, marketplace, product_name, product_url,
             card_price_with_discount, card_price_without_discount,
             product_description, quantity_of_goods)
        )

        connection.commit()
        print('Object already download to table')

    except Exception as _ex:
        print(_ex)

    finally:
        if connection:
            connection.close()

