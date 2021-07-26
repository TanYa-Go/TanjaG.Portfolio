## Testing user stories



## Testing Functionality

 ### **Testing links and buttons**

#### Navigation

- Top navigation fully functional, all links lead to the relevant section on the page
- When user scrolls down the navar dissapaear and when they scroll up the navbar will reappaer
- Mobile navigation toggle "hamburger" working as expecting, opening the navigation on smaller screens


 #### Hello Section 

 - Scroll down button functioning as expected, scrolls down when clicked
 - Social media icons open the respective page in the new tab

 
#### Skills

- When logged in as admin user can see the **edit** and **delete** icons beside each skill. Tooltip will pop up to give the user infomation what each button does, in case is not clear from the icons
- Buttons work as expected, sending user to edit skill or deleting the skill
- Those buttons are not visible to the non-admin user 

#### Projects 

- **View Website** nand **View Repo** buttons work as intended, lead the user to the respective page, opening it in the new tab

#### Testimonials

- When logged in as admin user can see the **edit** and **delete** icons under each testimonial. Tooltip will pop up to give the user infomation what each button does, in case is not clear from the icons
- Buttons work as expected, sending user to edit skill or deleting the skill
- Those buttons are not visible to the non-admin user 

#### Footer 
 - Click on the arrow icon in the footer opens a .pdf file of the CV in the separate tab where user can download it
- Social links are functioning properly, opening the page in a new tab
- Click on the email address will immediately open the users email provider to send an email directly

#### Register/Login

- Register and Login both have the button to submit the respective action. Both buttons function as intended and send the user to the dashboard while the respective flash message appears on the screen 
- Register and Login links are  removed from the navbar but can be accessed by inputting the right path in the url  /register or /login

#### Logout

- Logout button functions as intended, sends the user back to the login page while flash message appears confriming to the user that they have been logged out
- Logout link is removed from the navbar but can be accessed by inputting the right url path /logout

#### Dashboard

- By clicking on the **Add Skill**, **Edit Skill**, **Add Testimonial** or **Edit Testimonial** button on the Dashboard, the user is redirected to the respective page

<br>  

 ### **Testing form Validation**