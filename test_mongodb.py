from database.mongodb import client, db

try:
    client.admin.command("ping")
    print("MongoDB connected successfully!")

    print("Database:", db.name)
    print("Collections:", db.list_collection_names())

except Exception as error:
    print("MongoDB connection failed:")
    print(error)

finally:
    client.close()