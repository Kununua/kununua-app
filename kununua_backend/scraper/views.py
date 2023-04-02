from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from scraper.utils.ClassificatorSQLiteAPI import ClassificatorSQLiteAPI
from scraper.models import ProductScraped




def matching_training_view(request):
    API = ClassificatorSQLiteAPI()
    if request.method == "POST":
        prod1_id = request.POST['prod1_id']
        prod2_id = request.POST['prod2_id']
        matching = request.POST['matching']
        
        print(prod1_id, prod2_id, matching)
        
        API.update_match(prod1_id, prod2_id, matching)
        
    possible_matches = API.get_possible_matches(condition="is_match IS NULL")
                
        # Add to database
    
    if not possible_matches:
        render(request, "matching_training.html", {"message": "No more matches to train"})
    
    possible_match = possible_matches.pop(0)

    products = API.get_products_scraped(condition=f"id IN ({possible_match[1]}, {possible_match[2]})")
    
    products_scraped = _parse_classificator_sqlite_products(products)
    
    prod1 = products_scraped[0]
    prod2 = products_scraped[1]
        
    return render(request, 'matching_training.html', context={"product1": prod1, "product2": prod2})
    
def _parse_classificator_sqlite_products(sqlite_products):
    return [ProductScraped(
                                        pseudo_id = int(product[0]),
                                        name=str(product[1]),
                                        price=float(product[2]),
                                        unit_price=str(product[3]) if product[3] else None,
                                        weight=str(product[4]) if product[4] else None,
                                        brand=str(product[5]) if product[5] else None,
                                        amount=int(product[6]) if product[6] else None,
                                        image=str(product[7]),
                                        offer_price=float(product[8]) if product[8] else None,
                                        is_vegetarian=bool(product[9]),
                                        is_gluten_free=bool(product[10]),
                                        is_freezed=bool(product[11]),
                                        is_from_country=bool(product[12]),
                                        is_eco=bool(product[13]),
                                        is_without_sugar=bool(product[14]),
                                        is_without_lactose=bool(product[15]),
                                        url=str(product[16]) if product[16] else None,
                                        is_pack=bool(product[17]),
                                        category=str(product[18]),
                                        supermarket=str(product[19]),
                                        )
                                    for product in sqlite_products
                                ]