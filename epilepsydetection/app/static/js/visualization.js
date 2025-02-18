let renderer, renderWindow, openGLRenderWindow, interactor, actor, mapper;

function initVTK() {
    const container = document.getElementById('vtkContainer');

    renderer = vtk.Rendering.Core.vtkRenderer.newInstance();
    renderWindow = vtk.Rendering.Core.vtkRenderWindow.newInstance();
    renderWindow.addRenderer(renderer);

    openGLRenderWindow = vtk.Rendering.OpenGL.vtkRenderWindow.newInstance();
    renderWindow.addView(openGLRenderWindow);
    openGLRenderWindow.setContainer(container);

    interactor = vtk.Rendering.Core.vtkRenderWindowInteractor.newInstance();
    interactor.setView(openGLRenderWindow);
    interactor.initialize();
    interactor.bindEvents(container);

    fetch('/get_mesh_data')
        .then(response => response.json())
        .then(data => {
            const reader = vtk.IO.Core.vtkPolyDataReader.newInstance();
            reader.parseAsArrayBuffer(data);

            mapper = vtk.Rendering.Core.vtkMapper.newInstance();
            mapper.setInputData(reader.getOutputData());

            actor = vtk.Rendering.Core.vtkActor.newInstance();
            actor.setMapper(mapper);

            renderer.addActor(actor);
            renderer.resetCamera();
            renderWindow.render();
        });
}

initVTK();
