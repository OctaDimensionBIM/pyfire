import clr
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Structure import *

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# Start a transaction
t = Transaction(doc, 'Place Sprinklers')
t.Start()

# Get all MEP spaces in the document
collector = FilteredElementCollector(doc)
spaces = collector.OfClass(SpatialElement).OfCategory(BuiltInCategory.OST_MEPSpaces)

# Loop through each space
for space in spaces:
    # Get the value of the NOS parameter
    nos_param = space.LookupParameter('NOS')
    if nos_param:
        nos_value = nos_param.AsInteger()
        print('NOS value for space {}: {}'.format(space.Id, nos_value))
        # Get the bounding box of the space
        bounding_box = space.get_BoundingBox(None)
        if bounding_box is None:
            print('Could not get bounding box for space.')
            continue
        # Get the floor level of the space
        level = doc.GetElement(space.LevelId)
        if level is None:
            print('Could not get level for space.')
            continue
        floor_elevation = level.Elevation
        # Calculate the spacing between sprinklers
        x_spacing = bounding_box.Max.X - bounding_box.Min.X
        y_spacing = bounding_box.Max.Y - bounding_box.Min.Y
        if nos_value > 1:
            x_spacing /= (nos_value - 1)
            y_spacing /= (nos_value - 1)
        else:
            x_spacing = 0
            y_spacing = 0
        # Loop through each sprinkler and place it in the space
        for i in range(nos_value):
            # Get the family symbol of the sprinkler
            sprinkler_type_id = None
            collector = FilteredElementCollector(doc)
            collector.OfCategory(BuiltInCategory.OST_Sprinklers)
            collector.OfClass(FamilySymbol)
            for elem in collector:
                if elem.FamilyName == "Sprinkler - Pendent":
                    sprinkler_type_id = elem.Id
                    break
            if sprinkler_type_id is None:
                print('Could not find a suitable sprinkler family.')
                continue
            sprinkler_type = doc.GetElement(sprinkler_type_id)
            # Calculate the location of the sprinkler
            x = bounding_box.Min.X + i * x_spacing
            y = bounding_box.Min.Y + i * y_spacing
            z = floor_elevation + 7 # set sprinkler height to 7 ft from MEP space floor level
            location_point = XYZ(x, y, z)
            # Create a new family instance for the sprinkler
            new_sprinkler = doc.Create.NewFamilyInstance(location_point, sprinkler_type, space, StructuralType.NonStructural)

# Commit the transaction
t.Commit()
#hence Completed
