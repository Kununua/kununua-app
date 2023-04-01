from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def matching_training_view(request):
    
    if request.method == "POST":
        prod1_id = request.POST['prod1_id']
        prod2_id = request.POST['prod2_id']
        matching = request.POST['matching']
        
        print(matching)
        
        # Add to database
        
    prod1 = {
            "id": 1,
            "name": "Product 1",
            "price": 1.0,
            "unit_price": "1.0€/gr",
            "weight": "1.0gr",
            "brand": "Brand 1",
            "amount": None,
            "image": "https://www.supermercadoseljamon.com/documents/10180/892067/37005200_M.jpg",
            "offer_price": None,
            "url": "https://www.supermercadoseljamon.com/detalle/-/Producto/filtros-1x4-40ud/37005200",
            "is_pack": False,
            "category": "Despensa",
            "supermarket": "Mecadona"
        }
    
    prod2 = {
            "id": 2,
            "name": "Product 2",
            "price": 3.0,
            "unit_price": "3.0€/kg",
            "weight": "3kg",
            "brand": "Brand 2",
            "amount": None,
            "image": "https://www.supermercadoseljamon.com/documents/10180/892067/37005200_M.jpg",
            "offer_price": None,
            "url": "https://www.supermercadoseljamon.com/detalle/-/Producto/filtros-1x4-40ud/37005200",
            "is_pack": False,
            "category": "Despensa",
            "supermarket": "Mecadona"
        }
        
    return render(request, 'matching_training.html', context={"product1": prod1, "product2": prod2})
    
