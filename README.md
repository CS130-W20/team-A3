# EducationAI

> EduAI, a website to help people learn and explore MOOCs in a more efficient way. 

[![Build Status][travis-image]][travis-url]

Our application will have two primary novel features:
1) Features for exploring MOOCs based on knowledge concept dependencies. 
2) Personalized learning. Learners have various backgrounds, and traditional platforms ignore this diversity by suggesting the same courses for every learner.

![](Screenshot.png)

## Installation

OS X & Linux & Windows:

```sh
python application.py
```


## Usage example
Go to http://0.0.0.0:8080 by default. You can enter the browse mode. Search the relevant concept such as machine learning on the above search bar, you can find relevant courses to the concept. 


## Release History

* Part C
    * Basic functional logics done 
* Part B 
    * Basic Templates Done 
* Part A
    * Work in Progress


## Contributing

1. Fork it 
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

<!-- Markdown link & img dfn's -->
[npm-image]: https://img.shields.io/npm/v/datadog-metrics.svg?style=flat-square
[npm-url]: https://npmjs.org/package/datadog-metrics
[npm-downloads]: https://img.shields.io/npm/dm/datadog-metrics.svg?style=flat-square
[travis-image]: https://img.shields.io/travis/dbader/node-datadog-metrics/master.svg?style=flat-square
[travis-url]: https://travis-ci.org/dbader/node-datadog-metrics
[wiki]: https://github.com/yourname/yourproject/wiki

## Note
* To meet the course requirement for Part C, we re-committed our repo at Feb. 18. Please just ingore all the previous records before that day. (@Professor, @TA)


## Code structure.

* code
	* This file is for the functional codes, including data crawl and database construction.
	
	* /crawler
		* crawl.py
			* course data crawl.
		* index_module.py
			* build the inverted index database for search. 
	* /auth
		* __init__.py
			* initialization file for auth
		* controller.py
			* functions related to user management.
		* models.py
			* define user class.
	* /browse
		* __init__.py
			* initialization file for browse mode.
		* controller.py
			* functions related to browse mode.
		* generate_categories.py
			* Parse the original course_taxonomy into sturctured data.
	* /search
		* __init__.py
			* initialization file for search mode.
		* controller.py
			* functions related to search mode.
		* search_engine.py
			* search engine class.
		* utils.py
			* Define utility functions for search module.
	* /testing
		* all_test.py
			* test all functions.
		* browse_test.py
			* test browse mode.
		* graph_test.py
			* test concept graph.
		* login_test.py
			* test login
		* logout_test.py
			* test logout.
		* search_test.py
			* test search
		* signup_test.py
			* test sign up.
		* userdesc_test.py
			* test user description
		* userimage_test.py
			* test user image.
		* userinfo_test.py
			* test user information.
	* /users

		* __init__.py
			* initialization file for user.
		* controller.py
			* Controller for user home page
		* /modules
			* education.py
				* Provide education level list for frontend.
			* history,py
				* Provide user history for frontend.
			* interests.py
				* Provide interest list for frontend.
			* portfolio.py 
				* user information stored in database.
			* recommendation.py
				* recommend a course to user.

	* /visualization
		* __init__.py
			* initialization file for the visualization module.
		* controllers.py
			* functionality in visualization.

	* application.py
			* The main file
	* config.py
		* setting of support files.
	* config.ini 
		* instantiation of support files
	* __init__.py
		* homepage backend.
	* /static
		* resources for frontend.
	* /templates
		* templates for frontend.
	* requirements.txt
		* dependent libraries 








