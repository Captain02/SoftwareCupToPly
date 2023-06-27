import vtk
from trimesh.exchange.obj import export_obj

def read_nii(filename):
    '''
    读取nii文件，输入文件路径
    '''
    reader = vtk.vtkNIFTIImageReader()
    reader.SetFileName(filename)
    reader.Update()
    return reader


def get_mc_contour(file, setvalue):
    '''
    计算轮廓的方法
    file:读取的vtk类
    setvalue:要得到的轮廓的值
    '''
    contour = vtk.vtkDiscreteMarchingCubes()
    contour.SetInputConnection(file.GetOutputPort())

    contour.ComputeNormalsOn()
    contour.SetValue(0, setvalue)
    return contour


def smoothing(smoothing_iterations, pass_band, feature_angle, contour):
    '''
    使轮廓变平滑
    smoothing_iterations:迭代次数
    pass_band:值越小单次平滑效果越明显
    feature_angle:暂时不知道作用
    '''
    # vtk有两种平滑函数，效果类似
    # vtk.vtkSmoothPolyDataFilter()
    # smoother = vtk.vtkSmoothPolyDataFilter()
    # smoother.SetInputConnection(contour.GetOutputPort())
    # smoother.SetNumberOfIterations(50)
    # smoother.SetRelaxationFactor(0.6)    # 越大效果越明显

    # vtk.vtkWindowedSincPolyDataFilter()
    smoother = vtk.vtkWindowedSincPolyDataFilter()
    smoother.SetInputConnection(contour.GetOutputPort())
    smoother.SetNumberOfIterations(smoothing_iterations)
    smoother.BoundarySmoothingOff()
    smoother.FeatureEdgeSmoothingOff()
    smoother.SetFeatureAngle(feature_angle)
    smoother.SetPassBand(pass_band)
    smoother.NonManifoldSmoothingOn()
    smoother.NormalizeCoordinatesOn()
    smoother.Update()
    return smoother


def singledisplay(obj):
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(obj.GetOutputPort())
    mapper.ScalarVisibilityOff()

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    renderer = vtk.vtkRenderer()
    renderer.SetBackground([0.1, 0.1, 0.5])
    renderer.AddActor(actor)
    window = vtk.vtkRenderWindow()
    window.SetSize(512, 512)
    window.AddRenderer(renderer)

    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(window)

    # 开始显示
    window.Render()
    interactor.Initialize()
    interactor.Start()
    export_obj(window)
    return window


def multidisplay(obj):
    # This sets the block at flat index 3 red
    # Note that the index is the flat index in the tree, so the whole multiblock
    # is index 0 and the blocks are flat indexes 1, 2 and 3.  This affects
    # the block returned by mbds.GetBlock(2).
    colors = vtk.vtkNamedColors()
    mapper = vtk.vtkCompositePolyDataMapper2()
    mapper.SetInputDataObject(obj)
    cdsa = vtk.vtkCompositeDataDisplayAttributes()
    mapper.SetCompositeDataDisplayAttributes(cdsa)
    # 上色
    mapper.SetBlockColor(3, colors.GetColor3d('Red'))
    mapper.SetBlockColor(1, colors.GetColor3d('LavenderBlush'))
    mapper.SetBlockColor(2, colors.GetColor3d('Lavender'))
    mapper.SetBlockColor(4, colors.GetColor3d('Green'))
    mapper.SetBlockColor(5, colors.GetColor3d('Yellow'))
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    # Create the Renderer, RenderWindow, and RenderWindowInteractor.
    renderer = vtk.vtkRenderer()
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.AddRenderer(renderer)
    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)

    # Enable user interface interactor.
    renderer.AddActor(actor)
    renderer.SetBackground(colors.GetColor3d('SteelBlue'))
    renderWindow.SetWindowName('CompositePolyDataMapper')
    renderWindow.Render()
    renderWindowInteractor.Start()


def singledisplay(obj):
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(obj.GetOutputPort())
    mapper.ScalarVisibilityOff()

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    renderer = vtk.vtkRenderer()
    renderer.SetBackground([0.1, 0.1, 0.5])
    renderer.AddActor(actor)
    window = vtk.vtkRenderWindow()
    window.SetSize(512, 512)
    window.AddRenderer(renderer)

    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(window)

    # 开始显示
    window.Render()
    interactor.Initialize()
    interactor.Start()
    export_obj(window)
    return window


def write_ply(obj, save_dir, color):
    '''
    输入必须是单个模型，vtkMultiBlockDataSet没有GetOutputPort()类
    '''

    plyWriter = vtk.vtkPLYWriter()
    plyWriter.SetFileName(save_dir)
    plyWriter.SetColorModeToUniformCellColor()
    plyWriter.SetColor(color[0], color[1], color[2])
    plyWriter.SetInputConnection(obj.GetOutputPort())
    plyWriter.Write()

def multidisplay(obj):
    # This sets the block at flat index 3 red
    # Note that the index is the flat index in the tree, so the whole multiblock
    # is index 0 and the blocks are flat indexes 1, 2 and 3.  This affects
    # the block returned by mbds.GetBlock(2).
    colors = vtk.vtkNamedColors()
    mapper = vtk.vtkCompositePolyDataMapper2()
    mapper.SetInputDataObject(obj)
    cdsa = vtk.vtkCompositeDataDisplayAttributes()
    mapper.SetCompositeDataDisplayAttributes(cdsa)
    # 上色
    mapper.SetBlockColor(3, colors.GetColor3d('Red'))
    mapper.SetBlockColor(1, colors.GetColor3d('LavenderBlush'))
    mapper.SetBlockColor(2, colors.GetColor3d('Lavender'))
    mapper.SetBlockColor(4, colors.GetColor3d('Green'))
    mapper.SetBlockColor(5, colors.GetColor3d('Yellow'))
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    # Create the Renderer, RenderWindow, and RenderWindowInteractor.
    renderer = vtk.vtkRenderer()
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.AddRenderer(renderer)
    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)

    # Enable user interface interactor.
    renderer.AddActor(actor)
    renderer.SetBackground(colors.GetColor3d('SteelBlue'))
    renderWindow.SetWindowName('CompositePolyDataMapper')
    renderWindow.Render()
    renderWindowInteractor.Start()


if __name__ == '__main__':
    # 相关参数
    nii_dir = 'l.nii.gz'
    save_dir = 'nii/'
    smoothing_iterations = 100
    pass_band = 0.005
    feature_angle = 120
    reader = read_nii(nii_dir)

    color = [(0, 0, 0), (128, 0, 0), (0, 128, 0), (128, 128, 0), (0, 0, 128), (128, 0, 128), (0, 128, 128),
             (128, 128, 128), (64, 0, 0), (192, 0, 0), (64, 128, 0), (192, 128, 0), (64, 0, 128), (192, 0, 128),
             (64, 128, 128), (192, 128, 128), (0, 64, 0), (128, 64, 0), (0, 192, 0), (128, 192, 0), (0, 64, 128),
             (128, 64, 12)]

    mbds = vtk.vtkMultiBlockDataSet()
    mbds.SetNumberOfBlocks(5)
    items = ['1', '2', '3','4', '5', '6','7','8','9','10','11']
    for iter in range(1, 11):
        contour = get_mc_contour(reader, iter)
        smoothing_iterations = 30
        pass_band = 0.001
        feature_angle = 120
        smoother = smoothing(smoothing_iterations, pass_band,
                             feature_angle, contour)
        write_ply(smoother,  save_dir + f'{items[iter]}.ply', color[iter])

        mbds.SetBlock(iter, smoother.GetOutput())
        #

    # singledisplay(smoother)

    multidisplay(mbds)