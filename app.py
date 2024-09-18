import streamlit as st
import psycopg2 as pg

# Database connection
connection = pg.connect(
    dbname="freelance_job_marketplace",
    user="postgres",
    password="414618",
    port="5433"
)
cursor = connection.cursor()

# Set up session state to manage the display of login/signup pages
if 'page' not in st.session_state:
    st.session_state.page = 'home'  # Default page
if 'user_id' not in st.session_state:
    st.session_state.user_id = None  # Store user_id after login
if 'user_type' not in st.session_state:
    st.session_state.user_type = None  # Store user type after login

# Define page navigation functions
def show_login():
    st.session_state.page = 'login'

def show_signup():
    st.session_state.page = 'signup'

def show_home():
    st.session_state.page = 'home'

def show_dashboard():
    st.session_state.page = 'dashboard'

# Display title with a subtitle
st.title("🌐 Freelance Marketplace")
st.subheader("Connect with professionals to bring your ideas to life!")
st.markdown("---")  # Horizontal line for separation

# Show buttons only when on the homepage
if st.session_state.page == 'home':
    st.write("🔑 **Please sign in to continue or create a new account.**")
    
    # Create two columns for the buttons
    col1, col2 = st.columns(2)
    with col1:
        st.button("🔒 Sign In", on_click=show_login, help="Sign in with your existing account")
    with col2:
        st.button("🆕 Create New Account", on_click=show_signup, help="Create a new user account")

# Login functionality
if st.session_state.page == 'login':
    st.header("🔑 Sign In")
    st.write("Login with your credentials to access the marketplace.")

    # Create columns for better layout
    col1, col2 = st.columns(2)
    
    with col1:
        username = st.text_input("Username")
    with col2:
        password = st.text_input("Password", type="password")  # Hide the password input

    login = st.button("Login 🚀")
    
    
    if login:
        query = "SELECT user_id, user_type FROM Users WHERE username = %s AND pass = %s"
        cursor.execute(query, (username, password))
        result = cursor.fetchone()

        if result:
            st.session_state.user_id = result[0]
            st.session_state.user_type = result[1]  # Store the user type in session state
            
            # Debugging output to ensure correct user type is fetched
            st.write(f"User Type: {st.session_state.user_type}")

            st.success(f"🎉 Welcome back, **{username}**!")
            st.balloons()  # Add a balloon animation for successful login
            show_dashboard()  # Navigate to the dashboard
        else:
            st.error("❌ Invalid username or password.")
    
    st.button("⬅️ Back", on_click=show_home)

# Signup functionality
if st.session_state.page == 'signup':
    st.header("🆕 Create New Account")
    st.write("Fill in the details below to create a new user account.")

    # Create input fields for signup
    new_username = st.text_input("New Username")
    new_password = st.text_input("Create password", type="password")
    email = st.text_input("Enter your email id")
    user_type = st.radio("Select User Type", ["freelancer", "client"])
    
    signup = st.button("Signup 🚀")
    
    if signup:
        # Check if the username or email already exists
        cursor.execute("SELECT * FROM Users WHERE username = %s OR email = %s", (new_username, email))
        if cursor.fetchone():
            st.error("⚠️ Username or email already taken. Please try a different one.")
        else:
            # Insert new user
            try:
                query = "INSERT INTO Users (username, pass, email, user_type) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, (new_username, new_password, email, user_type))
                connection.commit()
                st.success(f"✅ User created successfully!")
                show_home()  # Navigate back to home after successful signup
            except Exception as e:
                st.error(f"❌ Error: {e}")
    
    st.button("⬅️ Back", on_click=show_home)

        
# Client and Freelancer Dashboard
if st.session_state.page == 'dashboard' and st.session_state.user_id:
    # Check if the user is a freelancer
    if st.session_state.user_type == 'freelancer':
        st.header("🧑‍💻 Freelancer Dashboard")
        # Greeting
        cursor.execute("SELECT username FROM Users WHERE user_id = %s", (st.session_state.user_id,))
        user_info = cursor.fetchone()
        user_name = user_info[0] if user_info else "Freelancer"

        st.subheader(f"👋 Hello, {user_name}! Welcome to your dashboard.")
        st.markdown("---")  # Horizontal line for separation

        # Tab layout for different sections
        tab_selection = st.selectbox("Select a tab:", ["Overview", "Available Jobs", "Applied Jobs"])

        if tab_selection == "Overview":
            # Dashboard Overview
            with st.expander("🛠️ Your Skills"):
                cursor.execute("SELECT skill_name FROM Skills WHERE freelancer_id = %s", (st.session_state.user_id,))
                skills = cursor.fetchall()

                if skills:
                    st.write(", ".join([skill[0] for skill in skills]))
                else:
                    st.write("🔍 You haven't added any skills yet.")

            with st.expander("📜 Job History"):
                cursor.execute("SELECT J.title, J.budget FROM Job_History JH JOIN Jobs J ON JH.job_id = J.job_id WHERE JH.freelancer_id = %s", (st.session_state.user_id,))
                job_history = cursor.fetchall()

                if job_history:
                    for job in job_history:
                        st.write(f"**Title:** {job[0]}")
                        st.write(f"**Budget:** ${job[1]}")
                else:
                    st.write("🗂️ You don't have any job history yet.")

            with st.expander("📝 Client Feedback"):
                cursor.execute("SELECT C.username, CF.feedback, CF.rating FROM Client_Feedback CF JOIN Users C ON CF.client_id = C.user_id WHERE CF.freelancer_id = %s", (st.session_state.user_id,))
                feedback = cursor.fetchall()

                if feedback:
                    for f in feedback:
                        st.write(f"**Client:** {f[0]}")
                        st.write(f"**Feedback:** {f[1]}")
                        st.write(f"**Rating:** {f[2]}/5 ⭐")
                else:
                    st.write("🗨️ No client feedback available.")

            with st.expander("📈 Freelancer Performance"):
                cursor.execute("SELECT J.title, FP.performance_rating FROM Freelancer_Performance FP JOIN Jobs J ON FP.job_id = J.job_id WHERE FP.freelancer_id = %s", (st.session_state.user_id,))
                performance = cursor.fetchall()

                if performance:
                    for p in performance:
                        st.write(f"**Job Title:** {p[0]}")
                        st.write(f"**Performance Rating:** {p[1]}/5 ⭐")
                else:
                    st.write("📊 No performance ratings available.")

        elif tab_selection == "Available Jobs":
            # Display available jobs
            st.subheader("📋 Available Jobs")
            cursor.execute("SELECT job_id, title, budget, status FROM Jobs WHERE status = 'open';")
            jobs = cursor.fetchall()

            if jobs:
                for job in jobs:
                    st.markdown(f"### Job ID: {job[0]}")
                    st.write(f"**Title:** {job[1]}")
                    st.write(f"**Budget:** ${job[2]}")
                    st.write(f"**Status:** {job[3]}")

                    # Apply for Job Button
                    with st.form(key=f"apply_form_{job[0]}"):
                        proposed_amount = st.number_input(f"Proposed Amount for Job {job[0]}", min_value=0, key=f"amount_{job[0]}")
                        submit_proposal = st.form_submit_button(f"Submit Proposal for Job {job[0]} 📝")
                        if submit_proposal:
                            cursor.execute("INSERT INTO Proposals (job_id, freelancer_id, proposed_amount, status) VALUES (%s, %s, %s, %s)",
                                           (job[0], st.session_state.user_id, proposed_amount, 'submitted'))
                            connection.commit()
                            st.success(f"✅ Applied for Job {job[0]} with proposed amount of ${proposed_amount}.")
            else:
                st.write("🚫 No available jobs at the moment.")

        elif tab_selection == "Applied Jobs":
            # Display applied jobs
            st.subheader("🗂️ Jobs You Applied For")
            cursor.execute("SELECT J.job_id, J.title, P.proposed_amount, P.status FROM Proposals P JOIN Jobs J ON P.job_id = J.job_id WHERE P.freelancer_id = %s", (st.session_state.user_id,))
            applied_jobs = cursor.fetchall()

            if applied_jobs:
                for job in applied_jobs:
                    st.markdown(f"### Job ID: {job[0]}")
                    st.write(f"**Title:** {job[1]}")
                    st.write(f"**Proposed Amount:** ${job[2]}")
                    st.write(f"**Status:** {job[3]}")
            else:
                st.write("🗑️ You haven't applied for any jobs yet.")

        st.markdown("---")  # Horizontal line for separation

        st.button("⬅️ Logout", on_click=show_home)
        

    elif st.session_state.user_type == 'client':
        st.header("🧑‍💼 Client Dashboard")

        # Fetch client information
        cursor.execute("SELECT username FROM Users WHERE user_id = %s", (st.session_state.user_id,))
        user_info = cursor.fetchone()
        user_name = user_info[0] if user_info else "Client"
        
        st.subheader(f"👋 Hello, {user_name}! Welcome to your dashboard.")
        st.markdown("---")  # Horizontal line for separation
        
        # Tab layout for different sections
        tab_selection = st.selectbox("Select a tab:", ["Overview", "Post a Job", "Manage Jobs"])

        if tab_selection == "Overview":
            with st.expander("📜 Your Job Posting History"):
                cursor.execute("SELECT job_id, title, budget, status FROM Jobs WHERE client_id = %s", (st.session_state.user_id,))
                job_history = cursor.fetchall()
                
                if job_history:
                    for job in job_history:
                        st.write(f"**Job ID:** {job[0]}")
                        st.write(f"**Title:** {job[1]}")
                        st.write(f"**Budget:** ${job[2]}")
                        st.write(f"**Status:** {job[3]}")
                        st.markdown("---")
                else:
                    st.write("🗂️ You haven't posted any jobs yet.")

        elif tab_selection == "Post a Job":
            st.subheader("📋 Post a New Job")
            job_title = st.text_input("Job Title")
            # job_description = st.text_area("Job Description")
            job_budget = st.number_input("Job Budget ($)", min_value=0)
            post_job = st.button("Post Job 🚀")

            if post_job:
                if job_title and job_budget:
                    # Insert the job into the Jobs table
                    try:
                        query = "INSERT INTO Jobs (title, budget, client_id, status) VALUES (%s, %s, %s, %s)"
                        cursor.execute(query, (job_title, job_budget, st.session_state.user_id, 'open'))
                        connection.commit()
                        st.success(f"✅ Job '{job_title}' posted successfully!")
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
                else:
                    st.error("⚠️ Please fill in all fields.")

        elif tab_selection == "Manage Jobs":
            st.subheader("🗂️ Manage Your Jobs")
            cursor.execute("SELECT job_id, title, budget, status FROM Jobs WHERE client_id = %s", (st.session_state.user_id,))
            jobs = cursor.fetchall()
            
            if jobs:
                for job in jobs:
                    st.markdown(f"### Job ID: {job[0]}")
                    st.write(f"**Title:** {job[1]}")
                    st.write(f"**Budget:** ${job[2]}")
                    st.write(f"**Status:** {job[3]}")
                    
                    # Show applications for this job
                    with st.expander(f"📋 View Applications for '{job[1]}'"):
                        cursor.execute("SELECT P.proposal_id, U.username, P.proposed_amount, P.status FROM Proposals P JOIN Users U ON P.freelancer_id = U.user_id WHERE P.job_id = %s", (job[0],))
                        applications = cursor.fetchall()

                        if applications:
                            for app in applications:
                                st.write(f"**Proposal ID:** {app[0]}")
                                st.write(f"**Freelancer:** {app[1]}")
                                st.write(f"**Proposed Amount:** ${app[2]}")
                                st.write(f"**Status:** {app[3]}")
                                st.markdown("---")
                        else:
                            st.write("🗂️ No applications for this job yet.")
                    
                    st.markdown("---")
            else:
                st.write("🚫 You have not posted any jobs yet.")

        st.button("⬅️ Logout", on_click=show_home)

    else:
        st.error("⚠️ You do not have access to this dashboard.")

