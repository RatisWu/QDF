# QDF
Quantum Data Formalizer. Formalize the raw data measured from QM or Qblox to a general format.

## Design cores
1.  Every experiment should own the same coordinates about the raw data dataset. And these coordinates are clearly registered.
2.  Suitable for different measurement system like QM, Qblox. 

## How to use
1.  Every experiment should own a unique converter class, which is named ExpName_dataConverter. For example, `FluxCavity_dataConverter()`.
2.  Give a Dataset or its file path and what system made, then use the method `transformExecutor(new_file_path)` to convert. If a new_file_path is given, the converted dataset will be saved there.
3.  The converted dataset can also be retrieved by the attribtue `ds` like `FluxCavity_dataConverter().ds`.
4.  See the last few lines in Converter.py for example.

## How to develop
1.  Register the ExpName as a method in Formalizer.DSCoordNameRegister(), it should named starting with '_' like `_FluxCavity()`. And the list of coordinate names is the return like ["mixer", "bias", "freq", "q_idx"].
2.  Build a new class in Converter.py which should inherite `QQAdapter()`. And this new class should be named by ExpName_dataConverter, ExpName here doesn't include '_'. For example, `FluxCavity_dataConverter()`.
3.  Design the inherited method `QB_adapter()` and 'QM_adapter()` and the converted dataset is the return of these methods.