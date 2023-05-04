"""sprinkler requirements"""
__title__ = 'Total Sprinklers'
import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
from Autodesk.Revit.UI import TaskDialog
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, Transaction, TransactionGroup, DisplayUnitType, BuiltInParameter, UnitUtils

doc = __revit__.ActiveUIDocument.Document

def get_spaces():
    return FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_MEPSpaces).ToElements()

def get_hazard_type(space):
    hazard_param = space.LookupParameter("HazardType")
    if hazard_param:
        hazard_type = hazard_param.AsString()
        return hazard_type

def calculate_sprinklers(area, hazard_type):
    if hazard_type == "Light":
        sprinklers = round(area / 200)
    elif hazard_type == "Ordinary":
        sprinklers = round(area / 130)
    elif hazard_type == "Extra":
        sprinklers = round(area / 90)
    else:
        sprinklers = None
    return sprinklers

t = TransactionGroup(doc, "Write Sprinklers to NOS Parameter")
t.Start()

updated_count = 0
for space in get_spaces():
    space_id = space.Id
    space_area = space.get_Parameter(BuiltInParameter.ROOM_AREA).AsDouble()
    hazard_type = get_hazard_type(space)
    if hazard_type:
        area_in_sqft = UnitUtils.ConvertFromInternalUnits(space_area, DisplayUnitType.DUT_SQUARE_FEET)
        sprinklers = calculate_sprinklers(area_in_sqft, hazard_type)
        if sprinklers:
            nos_param = space.LookupParameter("NOS")
            if nos_param:
                with Transaction(doc, "Set Sprinkler Count") as tx:
                    tx.Start()
                    nos_param.Set(sprinklers)
                    tx.Commit()
                updated_count += 1
    else:
        print("HazardType parameter not found for space ID: {}".format(space_id))

t.Commit()

if updated_count > 0:
    TaskDialog.Show("Sprinklers Updated", "Sprinkler counts have been updated for {} spaces.".format(updated_count))
else:
    TaskDialog.Show("No Sprinklers Updated", "No spaces were found with valid hazard types.")
