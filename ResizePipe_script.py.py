import clr
clr.AddReference("RevitAPI")
clr.AddReference("RevitAPIUI")

from Autodesk.Revit.DB import BuiltInParameter, Transaction, FilteredElementCollector, BuiltInCategory
from Autodesk.Revit.UI.Selection import Selection

# Get the active document and UIDocument
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# Define the fixture unit parameter
fixture_unit_param = BuiltInParameter.RBS_PIPE_FIXTURE_UNITS_PARAM

# Define the pipe size values in meters and corresponding fixture unit ranges
pipe_sizes = {
    0.0254: (0, 10),    # 1 inch
    0.03175: (10, 15),  # 1-1/4 inch
    0.0381: (15, 25),   # 1-1/2 inch
    0.0508: (25, 50),   # 2 inch
    0.0635: (50, 150),  # 2-1/2 inch
    0.0762: (150, 300), # 3 inch
    0.0889: (300, 500)  # 3-1/2 inch
}

# Get the selected pipe elements
selection = uidoc.Selection
pipe_refs = selection.GetElementIds()

# Start a transaction
transaction = Transaction(doc, "Change Pipe Sizes")
transaction.Start()

try:
    # Iterate over the selected pipe elements
    for pipe_ref in pipe_refs:
        pipe = doc.GetElement(pipe_ref)
        fixture_unit = pipe.get_Parameter(fixture_unit_param)

        if fixture_unit:
            # Access the parameter value
            fixture_unit_value = fixture_unit.AsDouble()

            # Find the exact pipe size based on the fixture unit value
            pipe_size = None
            for size, (lower_bound, upper_bound) in pipe_sizes.items():
                if lower_bound < fixture_unit_value <= upper_bound:
                    pipe_size = size
                    break

            if pipe_size is not None:
                # Change the pipe diameter parameter value based on pipe size
                pipe_size_param = pipe.get_Parameter(BuiltInParameter.RBS_PIPE_DIAMETER_PARAM)
                if pipe_size_param:
                    pipe_size_param.Set(pipe_size * 3.301724137931034)

                # Print the pipe element ID, fixture unit value, and pipe size
                print("Pipe Element ID:", pipe.Id)
                print("Fixture Unit:", fixture_unit_value)
                print("Pipe Size: {:.3f}".format(pipe_size))
                print("---")
            else:
                print("No matching pipe size found for Fixture Unit:", fixture_unit_value)

    # Commit the transaction
    transaction.Commit()

except Exception as ex:
    # Rollback the transaction in case of any exception
    transaction.RollBack()
    print("An error occurred:", str(ex))
