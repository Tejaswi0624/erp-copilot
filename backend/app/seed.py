"""
Seed script — runs once on startup if data doesn't already exist.
Creates demo users, departments, employees, products, customers,
invoices, work orders, and sample transactions.
"""
from datetime import date, datetime, timedelta
from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.models.user import User
from app.models.finance import Account, Transaction, Invoice, Budget
from app.models.hr import Department, Employee, Payroll, LeaveRequest
from app.models.inventory import Warehouse, Product, StockMovement, PurchaseOrder
from app.models.sales import Customer, SalesOrder, SalesOrderItem, Opportunity
from app.models.crm import Contact, Lead, Activity
from app.models.manufacturing import WorkOrder, BillOfMaterials, ProductionRun


def seed_all(db: Session):
    if db.query(User).first():
        return  # Already seeded
    print("🌱 Seeding demo data...")

    # ── Users ─────────────────────────────────────────────────────────────────
    users = [
        User(username="admin", email="admin@erp.com", full_name="Admin User",
             hashed_password=get_password_hash("admin123"), role="admin", is_active=True),
        User(username="finance", email="finance@erp.com", full_name="Finance Manager",
             hashed_password=get_password_hash("finance123"), role="finance", is_active=True),
        User(username="hr", email="hr@erp.com", full_name="HR Manager",
             hashed_password=get_password_hash("hr123"), role="hr", is_active=True),
        User(username="sales", email="sales@erp.com", full_name="Sales Manager",
             hashed_password=get_password_hash("sales123"), role="sales", is_active=True),
    ]
    db.add_all(users)
    db.flush()

    # ── Departments ───────────────────────────────────────────────────────────
    depts = [
        Department(name="Engineering", code="ENG", budget=500000),
        Department(name="Sales", code="SAL", budget=300000),
        Department(name="Finance", code="FIN", budget=200000),
        Department(name="Human Resources", code="HR", budget=150000),
        Department(name="Operations", code="OPS", budget=250000),
        Department(name="Marketing", code="MKT", budget=180000),
    ]
    db.add_all(depts)
    db.flush()

    # ── Employees ─────────────────────────────────────────────────────────────
    employees = [
        Employee(employee_id="EMP001", first_name="Alice", last_name="Johnson",
                 email="alice@erp.com", phone="+1-555-0101", position="Senior Engineer",
                 department_id=depts[0].id, salary=95000, hire_date=date(2020, 3, 15), status="active"),
        Employee(employee_id="EMP002", first_name="Bob", last_name="Williams",
                 email="bob@erp.com", phone="+1-555-0102", position="Sales Representative",
                 department_id=depts[1].id, salary=65000, hire_date=date(2021, 6, 1), status="active"),
        Employee(employee_id="EMP003", first_name="Carol", last_name="Davis",
                 email="carol@erp.com", phone="+1-555-0103", position="Financial Analyst",
                 department_id=depts[2].id, salary=78000, hire_date=date(2019, 11, 20), status="active"),
        Employee(employee_id="EMP004", first_name="David", last_name="Miller",
                 email="david@erp.com", phone="+1-555-0104", position="HR Specialist",
                 department_id=depts[3].id, salary=60000, hire_date=date(2022, 1, 10), status="active"),
        Employee(employee_id="EMP005", first_name="Eva", last_name="Wilson",
                 email="eva@erp.com", phone="+1-555-0105", position="Operations Manager",
                 department_id=depts[4].id, salary=88000, hire_date=date(2018, 7, 5), status="active"),
        Employee(employee_id="EMP006", first_name="Frank", last_name="Brown",
                 email="frank@erp.com", phone="+1-555-0106", position="Marketing Manager",
                 department_id=depts[5].id, salary=82000, hire_date=date(2020, 9, 14), status="active"),
        Employee(employee_id="EMP007", first_name="Grace", last_name="Taylor",
                 email="grace@erp.com", phone="+1-555-0107", position="Junior Engineer",
                 department_id=depts[0].id, salary=72000, hire_date=date(2023, 2, 1), status="active"),
        Employee(employee_id="EMP008", first_name="Henry", last_name="Anderson",
                 email="henry@erp.com", phone="+1-555-0108", position="Sales Manager",
                 department_id=depts[1].id, salary=90000, hire_date=date(2017, 4, 20), status="active"),
    ]
    db.add_all(employees)
    db.flush()
    # Update headcounts
    for d in depts:
        d.headcount = db.query(Employee).filter(Employee.department_id == d.id).count()

    # Leave requests
    db.add(LeaveRequest(employee_id=employees[1].id, leave_type="annual",
                        start_date=date(2025, 8, 1), end_date=date(2025, 8, 5), days=5,
                        reason="Family vacation", status="pending"))
    db.add(LeaveRequest(employee_id=employees[3].id, leave_type="sick",
                        start_date=date(2025, 7, 10), end_date=date(2025, 7, 11), days=2,
                        reason="Medical appointment", status="approved"))

    # ── Accounts ──────────────────────────────────────────────────────────────
    accounts = [
        Account(code="1001", name="Main Checking Account", account_type="asset", balance=285000, currency="USD"),
        Account(code="1002", name="Savings Account", account_type="asset", balance=150000, currency="USD"),
        Account(code="2001", name="Accounts Payable", account_type="liability", balance=45000, currency="USD"),
        Account(code="3001", name="Owner Equity", account_type="equity", balance=500000, currency="USD"),
        Account(code="4001", name="Sales Revenue", account_type="revenue", balance=0, currency="USD"),
        Account(code="5001", name="Operating Expenses", account_type="expense", balance=0, currency="USD"),
    ]
    db.add_all(accounts)
    db.flush()

    # Sample transactions (last 6 months)
    now = datetime.utcnow()
    for i in range(6):
        month_offset = timedelta(days=30 * i)
        db.add(Transaction(account_id=accounts[4].id, transaction_type="credit",
                           amount=45000 + i * 3000, category="Sales",
                           description=f"Monthly sales revenue",
                           date=now - month_offset))
        db.add(Transaction(account_id=accounts[5].id, transaction_type="debit",
                           amount=28000 + i * 1000, category="Operations",
                           description=f"Monthly operating expenses",
                           date=now - month_offset))

    # ── Invoices ──────────────────────────────────────────────────────────────
    invoices = [
        Invoice(invoice_number="INV-2025-001", customer_name="Acme Corp",
                customer_email="billing@acme.com", amount=12500, tax=1250, total=13750,
                status="paid", due_date=now - timedelta(days=15),
                paid_at=now - timedelta(days=10)),
        Invoice(invoice_number="INV-2025-002", customer_name="TechStart Inc",
                customer_email="ap@techstart.com", amount=8400, tax=840, total=9240,
                status="sent", due_date=now + timedelta(days=15)),
        Invoice(invoice_number="INV-2025-003", customer_name="Global Retail Ltd",
                customer_email="finance@globalretail.com", amount=22000, tax=2200, total=24200,
                status="overdue", due_date=now - timedelta(days=5)),
        Invoice(invoice_number="INV-2025-004", customer_name="Metro Services",
                customer_email="billing@metro.com", amount=5600, tax=560, total=6160,
                status="draft"),
        Invoice(invoice_number="INV-2025-005", customer_name="Prime Solutions",
                customer_email="accounts@prime.com", amount=18000, tax=1800, total=19800,
                status="paid", due_date=now - timedelta(days=30),
                paid_at=now - timedelta(days=25)),
    ]
    db.add_all(invoices)

    # ── Budgets ───────────────────────────────────────────────────────────────
    budgets = [
        Budget(name="Engineering Budget", department="Engineering", category="Salaries",
               allocated=500000, spent=320000, period="2025-Annual", year=2025),
        Budget(name="Sales Budget", department="Sales", category="Operations",
               allocated=300000, spent=180000, period="2025-Annual", year=2025),
        Budget(name="Marketing Budget", department="Marketing", category="Marketing",
               allocated=180000, spent=95000, period="2025-Annual", year=2025),
        Budget(name="IT Infrastructure", department="Engineering", category="Technology",
               allocated=120000, spent=67000, period="2025-Annual", year=2025),
    ]
    db.add_all(budgets)

    # ── Warehouse & Products ──────────────────────────────────────────────────
    wh = Warehouse(name="Main Warehouse", code="WH-01",
                   location="123 Industrial Blvd, Chicago, IL", capacity=5000)
    wh2 = Warehouse(name="East Coast Hub", code="WH-02",
                    location="456 Commerce St, Newark, NJ", capacity=3000)
    db.add_all([wh, wh2])
    db.flush()

    products = [
        Product(sku="SKU-001", name="Industrial Valve Type A", category="Components",
                unit_price=249.99, cost_price=120.00, quantity_on_hand=145,
                reorder_level=20, warehouse_id=wh.id),
        Product(sku="SKU-002", name="Control Panel 12V", category="Electronics",
                unit_price=599.99, cost_price=280.00, quantity_on_hand=8,
                reorder_level=15, warehouse_id=wh.id),
        Product(sku="SKU-003", name="Safety Helmet Pro", category="Safety",
                unit_price=89.99, cost_price=35.00, quantity_on_hand=0,
                reorder_level=50, warehouse_id=wh2.id),
        Product(sku="SKU-004", name="Hydraulic Pump 5000PSI", category="Machinery",
                unit_price=1499.99, cost_price=750.00, quantity_on_hand=22,
                reorder_level=5, warehouse_id=wh.id),
        Product(sku="SKU-005", name="Bearing Assembly 6205", category="Components",
                unit_price=45.99, cost_price=18.00, quantity_on_hand=320,
                reorder_level=100, warehouse_id=wh.id),
        Product(sku="SKU-006", name="Safety Gloves Cut Level D", category="Safety",
                unit_price=29.99, cost_price=12.00, quantity_on_hand=12,
                reorder_level=50, warehouse_id=wh2.id),
    ]
    db.add_all(products)
    db.flush()

    # Purchase orders
    db.add(PurchaseOrder(po_number="PO-2025-001", supplier_name="Industrial Supply Co",
                         supplier_email="orders@indsupply.com", total_amount=15000,
                         status="sent",
                         expected_date=now + timedelta(days=7)))
    db.add(PurchaseOrder(po_number="PO-2025-002", supplier_name="Safety Gear Ltd",
                         supplier_email="purchase@safetygear.com", total_amount=4500,
                         status="received",
                         expected_date=now - timedelta(days=3),
                         received_date=now - timedelta(days=1)))

    # ── Customers & Orders ────────────────────────────────────────────────────
    customers = [
        Customer(name="Acme Corporation", email="procurement@acme.com",
                 phone="+1-555-1001", company="Acme Corp", city="Chicago",
                 country="USA", credit_limit=100000, total_orders=12, total_revenue=148000),
        Customer(name="TechStart Inc", email="ops@techstart.com",
                 phone="+1-555-1002", company="TechStart Inc", city="San Francisco",
                 country="USA", credit_limit=50000, total_orders=5, total_revenue=42000),
        Customer(name="Global Retail Ltd", email="buying@globalretail.com",
                 phone="+44-20-7001", company="Global Retail Ltd", city="London",
                 country="UK", credit_limit=200000, total_orders=28, total_revenue=365000),
        Customer(name="Metro Services LLC", email="admin@metro.com",
                 phone="+1-555-1003", company="Metro Services", city="Dallas",
                 country="USA", credit_limit=75000, total_orders=7, total_revenue=63000),
    ]
    db.add_all(customers)
    db.flush()

    orders = [
        SalesOrder(order_number="SO-2025-001", customer_id=customers[0].id,
                   status="delivered", subtotal=12000, tax=1200, total=13200,
                   order_date=now - timedelta(days=30)),
        SalesOrder(order_number="SO-2025-002", customer_id=customers[2].id,
                   status="processing", subtotal=28500, tax=2850, total=31350,
                   order_date=now - timedelta(days=5)),
        SalesOrder(order_number="SO-2025-003", customer_id=customers[1].id,
                   status="confirmed", subtotal=8400, tax=840, total=9240,
                   order_date=now - timedelta(days=2)),
        SalesOrder(order_number="SO-2025-004", customer_id=customers[3].id,
                   status="draft", subtotal=5600, tax=560, total=6160),
    ]
    db.add_all(orders)
    db.flush()

    # Order items
    db.add(SalesOrderItem(order_id=orders[0].id, product_name="Industrial Valve Type A",
                          sku="SKU-001", quantity=20, unit_price=249.99, total=4999.80))
    db.add(SalesOrderItem(order_id=orders[0].id, product_name="Bearing Assembly 6205",
                          sku="SKU-005", quantity=100, unit_price=45.99, total=4599.00))
    db.add(SalesOrderItem(order_id=orders[1].id, product_name="Hydraulic Pump 5000PSI",
                          sku="SKU-004", quantity=10, unit_price=1499.99, total=14999.90))

    # Opportunities
    opportunities = [
        Opportunity(title="Acme Corp — Q3 Expansion Contract", customer_id=customers[0].id,
                    stage="negotiation", value=85000, probability=70,
                    expected_close=now + timedelta(days=30), owner="Henry Anderson"),
        Opportunity(title="TechStart — Annual Maintenance Agreement", customer_id=customers[1].id,
                    stage="proposal", value=24000, probability=55,
                    expected_close=now + timedelta(days=45), owner="Bob Williams"),
        Opportunity(title="New Prospect — City Council", customer_id=None,
                    stage="prospecting", value=150000, probability=20,
                    expected_close=now + timedelta(days=90), owner="Henry Anderson"),
        Opportunity(title="Global Retail — Equipment Upgrade", customer_id=customers[2].id,
                    stage="closed_won", value=62000, probability=100),
    ]
    db.add_all(opportunities)

    # ── CRM ───────────────────────────────────────────────────────────────────
    contacts = [
        Contact(first_name="John", last_name="Smith", email="john.smith@acme.com",
                phone="+1-555-2001", company="Acme Corp", position="Procurement Director",
                source="website"),
        Contact(first_name="Sarah", last_name="Chen", email="s.chen@techstart.com",
                phone="+1-555-2002", company="TechStart Inc", position="CTO",
                source="referral"),
        Contact(first_name="Marcus", last_name="Green", email="m.green@globalretail.com",
                phone="+44-20-7002", company="Global Retail Ltd", position="Buyer",
                source="trade_show"),
    ]
    db.add_all(contacts)
    db.flush()

    leads = [
        Lead(first_name="Linda", last_name="Park", email="l.park@startup.io",
             company="Startup IO", source="cold_call", status="contacted",
             estimated_value=15000, assigned_to="Bob Williams"),
        Lead(first_name="James", last_name="Turner", email="jturner@bigco.com",
             company="BigCo Ltd", source="website", status="new",
             estimated_value=45000, assigned_to="Henry Anderson"),
        Lead(first_name="Nina", last_name="Ross", email="nina@fastgrow.com",
             company="FastGrow Inc", source="referral", status="qualified",
             estimated_value=32000, assigned_to="Bob Williams"),
    ]
    db.add_all(leads)

    db.add(Activity(contact_id=contacts[0].id, activity_type="call",
                    subject="Follow-up call on Q3 contract", completed=True,
                    completed_at=now - timedelta(days=2)))
    db.add(Activity(contact_id=contacts[1].id, activity_type="meeting",
                    subject="Product demo scheduled",
                    due_date=now + timedelta(days=3), completed=False))

    # ── Manufacturing ─────────────────────────────────────────────────────────
    work_orders = [
        WorkOrder(wo_number="WO-2025-001", product_name="Industrial Valve Type A",
                  quantity=100, status="in_progress", priority="high",
                  start_date=now - timedelta(days=3), end_date=now + timedelta(days=4)),
        WorkOrder(wo_number="WO-2025-002", product_name="Hydraulic Pump 5000PSI",
                  quantity=20, status="planned", priority="normal",
                  start_date=now + timedelta(days=2), end_date=now + timedelta(days=10)),
        WorkOrder(wo_number="WO-2025-003", product_name="Control Panel 12V",
                  quantity=50, status="completed", priority="normal",
                  start_date=now - timedelta(days=20), end_date=now - timedelta(days=14),
                  completed_at=now - timedelta(days=14)),
    ]
    db.add_all(work_orders)
    db.flush()

    bom_items = [
        BillOfMaterials(product_name="Industrial Valve Type A", version="2.1",
                        component_name="Valve Body", component_sku="RAW-001", quantity=1, unit="pcs"),
        BillOfMaterials(product_name="Industrial Valve Type A", version="2.1",
                        component_name="Sealing Ring", component_sku="RAW-002", quantity=2, unit="pcs"),
        BillOfMaterials(product_name="Industrial Valve Type A", version="2.1",
                        component_name="Actuator Spring", component_sku="RAW-003", quantity=1, unit="pcs"),
    ]
    db.add_all(bom_items)

    db.add(ProductionRun(work_order_id=work_orders[2].id, quantity_planned=50,
                         quantity_produced=48, quantity_rejected=2,
                         operator="Eva Wilson", machine="Machine-03",
                         started_at=now - timedelta(days=20),
                         completed_at=now - timedelta(days=14)))

    db.commit()
    print("✅ Seed complete — admin/admin123, finance/finance123, hr/hr123, sales/sales123")
