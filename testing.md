## User Stories Testing

* ### **Recruiters and potential employers**

    * Users goal is to be able to find my skills and experience to see if it suits the role they have in mind.

        Skills and Education sections are displayed on the index page and can be accessed by scrolling down or by clicking on the navigation menu corresponding item.

        I have decided not to include the Work History details on the portfolio as I don't have the relevant experience yet. However, the user can see my previous employment by visiting my LinkedIn page or by accessing my CV from the footer. 

    * Users goal is to be able to see projects that I've worked on to see what type of work I've done and what are my competencies 

        My projects are displayed on the index page in the **My Projects** section and can be accessed by scrolling down or by clicking on the navigation menu corresponding item. To see more about each project, the user can click on the links below each project and access either the **live site** or **the repository** which will open in a separate tab.

    * Users goal is to see my previous employment to get a feel if someone my experience would be a good fit for their team

        I have decided not to include the Work History details on the portfolio, as explained above.

    * Users goal is to be able to find the contact information easily and contact me without leaving the page

        The user can find the contact information by clicking on the link in the navigation bar or scroll down to the footer. They will see the phone number, the email - which when clicked leads straight to the email provider so the user can send me an email without leaving the page. The user can also click on the LinkedIn icon which will lead to my LinkedIn page where they can also send me a message. 

    * User goal is to be able to download my CV with one click
     
      The user can click on the download icon in the footer which will open the .pdf document of my CV in the new tab where they can download it

* ### **Other developers** 

    * Users goal is to be able to find my GitHub profile to see the way I write my code and if this would suit their project

        The Github icon is available on the home page so it is easy to find. When clicked, the icon leads to my GitHub profile page, which opens in a new tab.
        There is also a GitHub link in the footer and on the downloadable CV.

* ### **Potential Clients** 
    * This user's goal is to be able to see the testimonials from others that have worked with me, to evaluate if they want to hire me

        The user can click on the Testimonials menu link in the navbar and will be redirected to the Testimonials section of the index page.

    
## Testing Functionality

 ### **Testing links and buttons**

#### Navigation

- Top navigation is fully functional, all links lead to the relevant section on the page
- When the user scrolls down the navbar disappear and when they scroll up the navbar will reappear
- Mobile navigation toggle "hamburger" working as expecting, opening the navigation on smaller screens


 #### Hello Section 

 - Scroll down button functioning as expected, scrolls down when clicked
 - Social media icons open the respective page in the new tab

 
#### Skills

- When logged in as an admin, the user can see the **edit** and **delete** icons beside each skill. A tooltip will pop up to give the user information on what each button does, in the case is not clear from the icons
- Buttons work as expected, sending the user to edit skill or deleting the skill
- Those buttons are not visible to the non-admin user 

#### Projects 

- **View Website** and **View Repo** buttons work as intended, lead the user to the respective page, opening it in the new tab

#### Testimonials

- When logged in as an admin, the user can see the **edit** and **delete** icons under each testimonial. A tooltip will pop up to give the user information on what each button does, in case is not clear from the icons
- Buttons work as expected, sending the user to edit skill or deleting the skill
- Those buttons are not visible to the non-admin user 

#### Footer 
 - Click on the arrow icon in the footer opens a .pdf file of the CV in the separate tab where the user can download it
- Social links are functioning properly, opening the page in a new tab
- Click on the email address will immediately open the user's email provider to send an email directly

#### Register/Login

- Register and log in both have the button to submit the respective action. Both buttons function as intended and send the user to the dashboard while the respective flash message appears on the screen 
- Register and Login links are  removed from the navbar but can be accessed by inputting the right path in the URL  /register or /login

#### Logout

- Logout button functions as intended, sends the user back to the login page while a flash message appears confirming to the user that they have been logged out
- Logout link is removed from the navbar but can be accessed by inputting the right URL path /logout

#### Dashboard

- By clicking on the **Add Skill**, **Edit Skill**, **Add Testimonial** or **Edit Testimonial** button on the Dashboard, the user is redirected to the respective page

<br>  

### Testing CRUD functionality for Skills and Testimonials
- **CREATE**: Create functionality was tested by clicking on the respective **Add Skill / Add Testimonial** buttons on the admin dashboard. After filling in the form the **Flash message** appears on the screen to confirm to the user that the Skill / Testimonial was successfully created. Under the flash message, there is a **View All Skills / View All Testimonials** link that leads to the respective section on the index page, so by clicking on this link the user can view the result of their action. There is no need to click on the **Home** in navigation or the **Back** arrow to see it. Skill / Testimonial are showing on the index page in their respective sections. Image upload works as expected. The functionality works as intended.

- **READ**: Skill / Testimonial including the images are showing on the index page in their respective sections.  The functionality works as intended.

-  **UPDATE**: Update functionality was tested by clicking on the **Edit Skill/Edit Testimonial** buttons on the admin dashboard. The user is redirected to the index page, the **Skills** or the **Testimonials** section where they can choose which item to edit. Once clicked on the **Edit** icon, the **Edit Form** page opens, prepopulated with that item data. Users can change one or all items. After clicking the **Add** button, a flash message appears confirming that the item was successfully updated. To view the change, the user can click on the **View All Skills / View All Testimonials** link. Results are satisfying, functionality works as intended.

- **DELETE**: Delete functionality was tested by clicking on the **Bin** icon beside the respective item on the index page.  The functionality works as intended, the item is deleted. 

 ### **Testing form Validation**