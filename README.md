# purchases
A database program created with the help of ChatGPT using GPT-4. 

There were a lot of issues along the way, and it does require some programming skills to make it work. But a lot of the generated code is excellent. 

One of the major issues was the frequently upcoming error: `network error`. This happens in the middle of the responses. You have to generate the response again and then you soon have filled your cap with no information receive. This means that you have to wait for 3 hours before you can continue. It becomes pretty inefficient, but I am still impressed about the final result. 

The communication with GPT-4 that eventually led up to this code can be found in the PDF file: "Successful database program code after many issues.pdf". Note that in addition to the generated code, it required some minor manual adjustments and corrections to run.

The database ended up having 4 tables. Here is the model:

1. People Table:
   - id (Primary Key)
   - name
   - email
   - phone


2. Items Table:
   - id (Primary Key)
   - item_name
   - price


3. Purchases Table:
   - id (Primary Key)
   - person_id (Foreign Key, referencing People.id)
   - timestamp


4. Purchase_items Table:
   - id (Primary Key)
   - purchases_id (Foreign Key, referencing Purchases.id)
   - item_id (Foreign Key, referencing Items.id)
   - quantity
   

<br/><br/>
   
   <img width="831" alt="image" src="https://user-images.githubusercontent.com/1498298/227059513-ed406ef7-af94-460a-806f-946b6b496a97.png">


<br/><br/>

A concrete example of how the tables could look with data populated is the following picture:

<br/><br/>

![Purchase Database (Custom)](https://user-images.githubusercontent.com/1498298/227155306-0c5d9822-6b1a-4149-8a4e-75bd1d72ac55.png)

<br/><br/>
