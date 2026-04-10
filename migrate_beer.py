from app import app, init_db
from models import db, Category, MLSize, Product, CategoryMLMapping

with app.app_context():
    print("Running init_db() to seed 650ml boundary...")
    init_db()
    print("init_db() completed.")

    beer_cat = Category.query.filter_by(name='Beer').first()
    ml_750 = MLSize.query.filter_by(value=750).first()
    ml_650 = MLSize.query.filter_by(value=650).first()

    if not beer_cat or not ml_750 or not ml_650:
        print("Error: Required foundational limits (Beer or ML identifiers) missing. Migration aborted.")
    else:
        legacy_products = Product.query.filter_by(category_id=beer_cat.id, ml_id=ml_750.id).all()
        print(f"Discovered {len(legacy_products)} Beer products flagged at 750ml.")

        migrated_count = 0
        for p in legacy_products:
            conflict = Product.query.filter_by(brand_name=p.brand_name, category_id=beer_cat.id, ml_id=ml_650.id).first()
            if conflict:
                print(f"Skipping {p.brand_name} ID={p.id} -> Duplicate already naturally populated on 650ml.")
            else:
                p.ml_id = ml_650.id
                migrated_count += 1
                print(f"Migrated {p.brand_name} cleanly.")
        
        db.session.commit()
        print(f"Migration successfully committed {migrated_count} objects to the database natively.")
