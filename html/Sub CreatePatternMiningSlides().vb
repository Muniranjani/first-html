Sub CreatePatternMiningSlides()
    ' Set up constants for slide layout and design
    Const SLIDE_LAYOUT_NAME = "My Layout"
    Const TEXT_BOX_WIDTH = 500
    Const TEXT_BOX_HEIGHT = 50
    Const TEXT_BOX_LEFT = 100
    Const TEXT_BOX_TOP = 100

    ' Set up PowerPoint application object
    Dim pptApp
    Set pptApp = CreateObject("PowerPoint.Application")

    ' Create a new presentation
    Dim pptPres
    Set pptPres = pptApp.Presentations.Add

    ' Set up slide layout and design
    Dim slideLayout
    Set slideLayout = pptPres.SlideMaster.CustomLayouts.Add(1)
    slideLayout.Name = SLIDE_LAYOUT_NAME

    ' Create an array of slide titles and contents
    Dim slideData
    slideData = Array( _
        Array("Classify Pattern Mining based on Pattern Diversity", "Introduction"), _
        Array("What is Pattern Mining?", "Pattern mining is the process of automatically discovering patterns in data."), _
        Array("Types of Pattern Mining", "1. Classification", "2. Clustering", "3. Association Rule Mining"), _
        Array("Classify Pattern Mining", "Classify pattern mining is a type of pattern mining that involves assigning a label or category to a pattern."), _
        Array("Pattern Diversity", "Pattern diversity refers to the variety of patterns present in a dataset."), _
        Array("Classify Pattern Mining based on Pattern Diversity", "Classify pattern mining based on pattern diversity involves assigning a label or category to a pattern based on its diversity.") _
    )

    ' Create slides using a loop
    Dim slide
    Dim i, j
    For i = 0 To UBound(slideData)
        Set slide = pptPres.Slides.Add(i + 1, 1)
        slide.Shapes.AddTextbox(1, TEXT_BOX_LEFT, TEXT_BOX_TOP, TEXT_BOX_WIDTH, TEXT_BOX_HEIGHT).TextFrame.TextRange.Text = slideData(i)(0)
        For j = 1 To UBound(slideData(i))
            slide.Shapes.AddTextbox(j + 1, TEXT_BOX_LEFT, TEXT_BOX_TOP + (j * 50), TEXT_BOX_WIDTH, TEXT_BOX_HEIGHT).TextFrame.TextRange.Text = slideData(i)(j)
        Next j
    Next i

    ' Save the presentation
    pptPres.SaveAs "C:\Users\R.MUNIRANJANI\Documents\Downloads\Presentation.pptx"

    ' Clean up
    Set pptPres = Nothing
    Set pptApp = Nothing
End Sub

' Call the subroutine to generate the slides
CreatePatternMiningSlides()
