# SOAP API Public Fetch Assignment

## Reflection

For this assignment, I worked on creating a SOAP client using Python, Flask, and Zeep. I started by setting up my project in Visual Studio Code and connecting it to a public SOAP web service using its WSDL. I then created GET and POST endpoints that allow users to enter numbers and receive a calculation result.

One thing I found interesting was how SOAP uses XML to exchange information, but Zeep can convert the response into a Python value that is easier to work with. I also added validation to make sure the numbers entered were within the required range. If someone enters an invalid number, the application displays a custom error message.

This assignment helped me better understand the differences between SOAP and REST APIs, especially how SOAP uses a defined service contract. Moving forward, I would like to learn more about handling SOAP faults and integrating SOAP services with other applications.
