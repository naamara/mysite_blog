
{% extends "personal/header.html" %}

{% block content %}

	<h1> Register With the system </h1>
	{% if registered %}
	the system says: <strong> thank you for registering! </strong>
	<a href ="/register/"> Return to the homepage.</a><br />
	{% else %}
	the system says: <strong> Register here! </strong> <br />

	<form id = "user_form" method="post" action ="" 
		enctype ="multipart/form-data">

		{% csrf_token %}

		#<!-- Display each form. the as_p method wraps each element in a paragraph (<p>) element. 
		#THis ensures each element appears on a new line, making everything look neater.-->
		{{ user_form.as_p }}
		{{ profile_form.as_p }}

		#provide a button to click to submit the form. 
		<input type="submit" name="submit" value ="Register" />
	</form>
	{% endif %}

{% endblock %}