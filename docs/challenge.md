--SPANISH

Parte 1: Desarrollo del Modelo

En esta parte del desafío, se ha desarrollado un modelo de Machine Learning para predecir retrasos en vuelos, basados en el cuaderno jupyter que se hizo entrega para transcribir este modelo. El modelo se basa en el algoritmo XGBoost, balanceando además las clases, y utiliza diversas características de los vuelos, como la hora del día, la temporada alta y la diferencia en minutos entre la hora de inicio y finalización del vuelo, para hacer predicciones. Se optó por elegir el modelo XGBoost ya que, al comparar los resultados de cada uno de los modelos propuestos en el cuaderno, si bien, la diferencia no era realmente significativa, era la que obtenía resultados ligeramente mejores al resto. Si bien, el modelo fue implementado en el archivo model.py, al realizar las pruebas se encontraron diversos fallos que no permitieron finalizar las pruebas correctamente. A pesar de depurar varias veces el código, notando que los parámetros entregados y recibidos eran los esperados, las pruebas continuaban arrojando fallos por motivos que se desconocen, lo que finalmente perjudica la ejecución de las siguientes pruebas.

Parte 2: Creación de la API (Creating the API)

En la segunda parte, se creó una API utilizando FastAPI, lo que permite a los usuarios enviar datos de vuelos y recibir predicciones de retrasos como respuesta. La API se encuentra en el archivo api.py y ofrece dos puntos finales: uno para verificar el estado de salud de la API y otro para realizar predicciones de retraso.

Parte 3: Implementación en Google App Engine (Deployment on Google App Engine)

En la tercera parte, se implementó la API en Google App Engine (GAE). Se configuró el archivo app.yaml para especificar la configuración de la aplicación, como la versión de Python y las variables de entorno necesarias. Luego, se utilizó la CLI de GAE para cargar la aplicación en la nube. Una vez implementada, se obtuvo una URL pública para acceder a la API en GAE.

Parte 4: CI/CD con GitHub Actions

Finalmente, en la cuarta parte, se implementó un flujo de trabajo de CI/CD (Integración Continua/Entrega Continua) utilizando GitHub Actions. Se crearon dos archivos YAML, ci.yml y cd.yml, para definir los flujos de trabajo de Integración Continua (CI) y Entrega Continua (CD). En estos flujos de trabajo, se configuraron pruebas automatizadas tanto para el modelo como para la API, así como despliegues automáticos en GAE cada vez que se realizaba una confirmación en la rama principal del repositorio.

A lo largo del proceso, se configuraron secretos en GitHub para proteger credenciales sensibles, como las credenciales de Google Cloud, y se utilizó el Makefile para automatizar tareas comunes como pruebas y despliegues.

Este desafío nos ha llevado a través de todo el ciclo de vida de desarrollo de un modelo de Machine Learning, la creación de una API, su implementación en la nube y la automatización de pruebas y despliegues con CI/CD. Cada parte del desafío ha sido una pieza crucial en la construcción de una aplicación de machine learning lista para producción.

--ENGLISH

Part 1: Model Development

In this part of the challenge, a Machine Learning model has been developed to predict flight delays. The model is based on the XGBoost algorithm, also balancing classes, and utilizes various flight features such as time of day, high seasonality, and the time difference in minutes between flight start and end times to make predictions. It was decided to choose the XGBoost model since, when comparing the results of each of the models proposed in the notebook, although the difference was not really significant, it was the one that obtained slightly better results than the rest. Although the model was implemented in the model.py file, when performing the tests, various errors were found that did not allow the tests to be completed correctly. Despite debugging the code several times, noting that the parameters delivered and received were as expected, the tests continued to fail for unknown reasons, which ultimately harmed the execution of the following tests.

Part 2: Creating the API

In the second part, an API was created using FastAPI, allowing users to submit flight data and receive delay predictions as responses. The API is located in the api.py file and offers two endpoints—one for checking the API's health status and another for making delay predictions.

Part 3: Deployment on Google App Engine

In the third part, the API was deployed on Google App Engine (GAE). The app.yaml file was configured to specify application settings such as the Python version and necessary environment variables. Subsequently, the GAE CLI was used to upload the application to the cloud. Once deployed, a public URL was obtained to access the GAE-hosted API.

Part 4: CI/CD with GitHub Actions

Finally, in the fourth part, a Continuous Integration/Continuous Delivery (CI/CD) workflow was implemented using GitHub Actions. Two YAML files, ci.yml and cd.yml, were created to define the Continuous Integration (CI) and Continuous Delivery (CD) workflows. Within these workflows, automated tests were configured for both the model and the API, and automatic deployments to GAE were set up for every commit to the main repository branch.

Throughout the process, secrets were configured in GitHub to safeguard sensitive credentials, such as Google Cloud credentials, and the Makefile was utilized to automate common tasks like testing and deployment.

This challenge has taken us through the entire development lifecycle of a Machine Learning model, the creation of an API, its cloud implementation, and the automation of testing and deployment with CI/CD. Each part of the challenge has been a crucial piece in constructing a production-ready machine learning application.