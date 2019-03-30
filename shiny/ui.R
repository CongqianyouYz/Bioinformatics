setwd("/Users/pengying/research/res/shiny_data")
library(shiny)
library(datasets)

dm6 <- read.table("data.dm6", header = T, sep = "\t")
ce10 <- read.table("data.ce10", header = T, sep = "\t")
hg38 <- read.table("data.hg38", header = T, sep = "\t")
mm10 <- read.table("data.mm10", header = T, sep = "\t")
danRer11 <- read.table("data.danRer11", header = T, sep = "\t")

ui <- fluidPage(
  titlePanel("RES INFO"),
  sidebarLayout(
    sidebarPanel(
      selectInput(inputId = "species",
        label = "Choose a datasets:",
        choices = c("ce10", "dm6", "hg38", "mm10", "danRer11")),
      
      selectInput("variable", "Variable:",
                  c("Tissue" = "Tissue",
                    "Develop_stage" = "Develop_stage",
                    "Sex" = "Sex",
                    "Disease" = "Disease",
                    "Ethnicity" = "Ethnicity")),
    
      checkboxInput("outliers", "Show outliers", TRUE)
    ),
    
    mainPanel(
      h3(textOutput("caption")),
      plotOutput("RESPlot")
    )
  )
)
