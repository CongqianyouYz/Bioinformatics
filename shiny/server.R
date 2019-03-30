setwd("/Users/pengying/research/res/shiny_data")
library(shiny)
library(datasets)

dm6 <- read.table("data.dm6", header = T, sep = "\t")
ce10 <- read.table("data.ce10", header = T, sep = "\t")
hg38 <- read.table("data.hg38", header = T, sep = "\t")
mm10 <- read.table("data.mm10", header = T, sep = "\t")
danRer11 <- read.table("data.danRer11", header = T, sep = "\t")

server <- function(input, output) {
  datasetInput <- reactive({
    switch(input$species,
           "ce10" = ce10,
           "danRer11" = danRer11,
           "dm6" = dm6,
           "hg38" = hg38,
           "mm10" = mm10)
  })
  
  formulaText <- reactive({
    paste("Editing_ratio ~", input$variable)
  })
  
  output$caption <- renderText({
    formulaText()
  })
  
  output$RESPlot <- renderPlot({
    raw_data <- datasetInput()
    switch(input$variable,
      Tissue = {
        my_data <- data.frame(raw_data$Editing_ratio, raw_data$Tissue)
        bymedian <- with(my_data, reorder(raw_data.Tissue,
                                          raw_data.Editing_ratio, median))
        },
      
      Develop_stage = {
        my_data <- data.frame(raw_data$Editing_ratio, raw_data$Develop_stage)
        bymedian <- with(my_data, reorder(raw_data.Develop_stage,
                                          raw_data.Editing_ratio, median))
      },
      
      Sex = {
        my_data <- data.frame(raw_data$Editing_ratio, raw_data$Sex)
        bymedian <- with(my_data, reorder(raw_data.Sex,
                                          raw_data.Editing_ratio, median))
      },
      
      Disease = {
        my_data <- data.frame(raw_data$Editing_ratio, raw_data$Disease)
        bymedian <- with(my_data, reorder(raw_data.Disease,
                                          raw_data.Editing_ratio, median))
      },
      
      Ethnicity = {
        my_data <- data.frame(raw_data$Editing_ratio, raw_data$Ethnicity)
        bymedian <- with(my_data, reorder(raw_data.Ethnicity,
                                          raw_data.Editing_ratio, median))
      }
      
    )
    
    par(mar = c(14, 3, 2.5, 0.5))
    
    boxplot(raw_data.Editing_ratio ~ bymedian,
            data = my_data,
            outline = input$outliers,
            main = paste("Species: ", input$species),
            col = "#75AADB", pch = 19, las = 2)
    
  })
}
