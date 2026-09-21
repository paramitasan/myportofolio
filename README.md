Name: **Paramita Santoso**

NPM: **2506554171**

Class: **KKI**<br></br>

### Description
This project is my portofolio website which displays my academic profile, interests, and many more. This site is built with HTML5, CSS3, and Django.<br></br>

---
### Week 3 - 21 Sep 2026
- Implemented skeleton (base.html) as the main layout framework
- Implemented forms (forms.py)
- Implemented data delivery with JSON
- Added create, edit, and delete feature in Education and Experience page
- Added a secret code to ensure that only I can edit the page<br></br>

###### Reflection
1. 
    a. Instead of creating HTML forms from scratch, we use Django's ModelForm because it provides the 'skeleton' of the form. It automatically generates HTML form fields from our database models, validates data using database constraint (e.g. Education `start_year` has to be 4 digits and has to be bigger than 2010), cleans user inputs safely, and generates error messages when invalid data is submitted.

    b.  `{% csrf_token %}` are required to be added into these forms because it generates a random, secret token for each soon-to-be created form. When submitted, Django compares this token against the user's session. If they don't match, the request is rejected. This prevents Cross-Site Request Forgery (CSRF) attacks.
2. JSON is more preferred in modern web application development compared to XML because JSON uses compact key-value pairs (`"title: MyTitle"`) without repetitive opening/closing tags (`<title> MyTitle </title>`), which is easier to read and lighter in size. Additionally, JavaScript can natively parse JSON without complex XML DOM parsers.
3. The flow that occurs when view function is used to return portfolio data in JSON format:
    - Request: client sends an HTTP GET request to a specific URL (e.g., `/api/experience/`).
    - Routing: urls.py routes the request to the designated view function (e.g., `get_experience_json`).
    - Query: The view retrieves data from the database (e.g., `Experience.objects.all()`), which returns a collection of Python model instances.
    - Serialization: The view passes these instances to `serializers.serialize("json", ...)` to convert the Python objects into JSON string.
    - Response: The serialized JSON string is returned as an `HttpResponse` (with `content_type="application/json"`) and sent back to the client.

We need to perform the serialization process on Django models before returning the data because serialization flattens complex database objects into a standardized, plain-text string structure (JSON) that can be sent over the internet and natively parsed by web browsers or frontend applications.<br></br>

###### AI Disclosure
I used Google Gemini to confirm the logic used in my code and help me debug error codes.

- Prompts:
    - "I would like to make the writing in the form to be different depends on whether it's editing or creating. if create it will show 'Add Education Record', if edit it will show 'Edit Education Record'. I want to change the text in some other place as well. does it use if else logic?"
    - "Why after I click delete record and enter password, data is still in page and not deleted?"
    - "Are the field type I put in ExperienceForm already compatible with the input received by model Experience? If no, please provide the correction and/or suggestions"
    - "When I open Experience page, this error shows. Please help me debug this and debug potential bugs. Do seperate them and explain to me why it can cause issues
    `Reverse for 'edit_experience' with arguments '('',)' not found. 1 pattern(s) tried: ['experience/(?P<exp_id>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/edit/\\Z']`"
- AI's Limitation & Manual Fix:
    - AI sometimes can't grasp the whole context of my code. When I asked to help solve my error, its suggestions leads to another error. Therefore, while I used AI's suggestion, I also debug it myself (using Django's traceback messages to identify missing variables or broken URL routing).

---
### Week 2 - 14 Sep 2026
- MTV (Model, Template, View) Django implementation
- Django unit test
- Added education and experience section<br></br>

###### Set up locally
1. Clone the repository:
    ```
    git clone https://github.com/paramitasan/myportofolio.git
    cd myportofolio
    ```

2. Create and activate a virtual environment:
    - MacOS/Linux
    ```
    python3 -m venv env
    source env/bin/activate
    ```
    - Windows
    ```
    python -m venv env
    env\Scripts\activate
    ```
3. Install the dependencies:
    ```
    pip install -r requirements.txt
    ```

4. Apply database migrations:
    ```
    python manage.py migrate
    ```

5. Run the server:
    ```
    python manage.py runserver
    ```
6. Open `http://127.0.0.1:8000/` in your browser

<br></br>
###### Reflection
1. When opening the new portofolio page (Education page), user clicks or enters the link http://127.0.0.1:8000/education/. The link will be accepted by project's urls.py (portofolio/urls.py) and directed to the app's urls.py (main/urls.py). In main/urls.py, the matching path (education/) is located, and the assigned view in main/views.py ("show_education") is executed. Inside the function, views.py obtains the needed data (i.e. Education.objects) through main/models.py (models.py fetches the data from the database). When the required data is complete, views.py passes it to the designated HTML template (education.html), which is the skeleton of the website. With tags like {% for %} and {{ edu.institution_name }}, Django compiles a dynamic HTML page. Finally, the view sends the compiled HTML page back to the browser, which renders it on screen.
2. Instead of writing the data for the new portfolio section directly in the template, storing the data in a model keeps data separate from page layout (HTML presentation). Design changes in templates won't affect stored data, and updating data won't risk breaking HTML structure. Additionally, it makes the code scalable. Whenever we have to add new data, we just need to add new object to the model, no need to edit the website layout.
3. makemigrations records the changes made to the model in models.py and creates migration blueprints in main/migrations. migrate reads the blueprint and make the changes to the database. For example, when I first made Education model without attribute description, models.py was updated, but my database isn't updated yet. Running `python manage.py makemigrations` generated the blueprint file for this update, and running `python manage.py migrate` actually made changes to the database table so it could store and retrieve descriptions without throwing an error. <br></br>

###### AI Disclosure
I used Google Gemini (hereafter referred as Gemini) to help me debug coding errors which caused my web not match my expectations. I also asked Gemini suggest improvements regarding my code, which helped reduce code duplication in my style.css file.
![AI_Disc_Assignment02_1](images/Assignment02_AI_2.png)


Lastly, I also asked Gemini to help solve an issue I could not address when creating unit tests.
![AI_Disc_Assignment02_2](images/Assignment02_AI_1.png)

---
### Week 1 - 07 Sep 2026
- Initial setup
- Added hero and skills section<br></br>

###### Reflection
1. I used 'section', one of HTML5's semantic elements, to help me clearly seperate between distinct parts within my portofolio website (i.e. "hero" and "skills"). Section "hero" consists of my introduction, so detailed information is put in a different section. In my case, I put some of my skills and their illustrations on section "skills".
Additionally, each section has a unique id which can be used as a hyperlink — to jump from the landing page to desired section.
2. When I set up my CSS to stay responsive, I had to make sure that my multicolumn item not get squished in small-screen view and ensure the images I put in section "skills" move dynamically according to the page size.
I decided that the elements needed to be prioritized are the images, because they are large in size and they are the most affected when page size are changed. 
I used CSS Grid so my skill images automatically drop down into a single line when the screen gets narrow.
3. Since the web is currently static, visitors can't really interact with the images and texts in my web. They can only see them. Hence, for future advancement, I would like to add clickable skill cards which can display more than just text (e.g. certificates).<br></br>

###### AI Disclosure
I used Google Gemini to assist me in checking and fixing my code skeleton layout, also to help me debug errors that occur in my code.
![AI_Disc_Assignment01](images/Assignment01_AI.png)