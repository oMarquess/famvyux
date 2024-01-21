# from SPARQLWrapper import SPARQLWrapper, JSON

# def get_movie_description(title):
#     url = 'https://query.wikidata.org/sparql'
#     user_agent = 'CoolBot/0.0 (https://example.org/coolbot/; coolbot@example.org)'

#     # Example SPARQL query (modify as needed)
#     query = """
#     SELECT ?movie ?movieLabel ?description WHERE {
#         ?movie wdt:P31 wd:Q11424;
#                rdfs:label ?movieLabel;
#                schema:description ?description.
#         FILTER(CONTAINS(LCASE(?movieLabel), LCASE("%s")))
#         FILTER(LANG(?movieLabel) = "en")
#         FILTER(LANG(?description) = "en")
#     } LIMIT 1
#     """ % title

#     sparql = SPARQLWrapper(url, agent=user_agent)
#     sparql.setQuery(query)
#     sparql.setReturnFormat(JSON)

#     try:
#         results = sparql.query().convert()
#         for result in results["results"]["bindings"]:
#             return result["description"]["value"]
#     except Exception as e:
#         print("Error: ", e)
#         return "No description available"

# # Example usage
# description = get_movie_description("Inception")
# print(description)
