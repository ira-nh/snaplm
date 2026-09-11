import onnxruntime as ort

import winui3.microsoft.windows.ai.machinelearning as winml

from winui3.microsoft.windows.applicationmodel.dynamicdependency.bootstrap import (
    InitializeOptions,
    initialize,
)


with initialize(options=InitializeOptions.ON_NO_MATCH_SHOW_UI):

    catalog = winml.ExecutionProviderCatalog.get_default()
    providers = catalog.find_all_providers()

    print("Compatible Windows ML Execution Providers")
    print("=========================================")
    print()

    for provider in providers:
        print(f"Name: {provider.name}")
        print(f"State: {provider.ready_state.name}")
        print(f"Library: {provider.library_path}")
        print()

    # Search the compatible providers for QNN
    qnn = None

    for provider in providers:
        if provider.name == "QNNExecutionProvider":
            qnn = provider
            break

    # Stop if QNN is not compatible with this machine
    if qnn is None:
        print("QNN Execution Provider is not compatible with this system.")
        raise SystemExit(1)

    print("QNN provider found.")
    print(f"Current state: {qnn.ready_state.name}")
    print("Preparing QNN...")

    # Make the QNN provider ready for use
    qnn.ensure_ready_async().get()

    print(f"New state: {qnn.ready_state.name}")
    print(f"Library: {qnn.library_path}")


    print()
    print("Registering QNN with ONNX Runtime...")

    ort.register_execution_provider_library(
        qnn.name,
        qnn.library_path,
    )

    print()
    print("Registered ONNX Runtime providers:")
    print(ort.get_available_providers())

# catalog = winml.ExecutionProviderCatalog.get_default()
# gets the catalogue of execution providers

# providers = catalog.find_all_providers()
# returns execution providers compatible with this machine