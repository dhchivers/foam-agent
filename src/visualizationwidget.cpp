#include "visualizationwidget.h"
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QLabel>
#include <QMessageBox>

VisualizationWidget::VisualizationWidget(CaseManager *manager, QWidget *parent)
    : QWidget(parent), caseManager(manager)
{
    setupUI();
}

VisualizationWidget::~VisualizationWidget()
{
}

void VisualizationWidget::setupUI()
{
    QVBoxLayout *mainLayout = new QVBoxLayout(this);
    
    // Control buttons
    controlGroup = new QGroupBox("Visualization Controls", this);
    QHBoxLayout *controlLayout = new QHBoxLayout();
    
    paraViewButton = new QPushButton("Launch ParaView", this);
    paraViewButton->setStyleSheet("QPushButton { background-color: #2196F3; color: white; font-weight: bold; padding: 15px; }");
    refreshButton = new QPushButton("Refresh Data", this);
    
    controlLayout->addWidget(paraViewButton);
    controlLayout->addWidget(refreshButton);
    controlGroup->setLayout(controlLayout);
    mainLayout->addWidget(controlGroup);
    
    // Data selection
    dataGroup = new QGroupBox("Data Selection", this);
    QVBoxLayout *dataLayout = new QVBoxLayout();
    
    dataLayout->addWidget(new QLabel("Time Step:"));
    timeStepCombo = new QComboBox(this);
    dataLayout->addWidget(timeStepCombo);
    
    dataLayout->addWidget(new QLabel("Available Fields:"));
    fieldList = new QListWidget(this);
    fieldList->setSelectionMode(QAbstractItemView::MultiSelection);
    dataLayout->addWidget(fieldList);
    
    dataGroup->setLayout(dataLayout);
    mainLayout->addWidget(dataGroup);
    
    // View options
    viewGroup = new QGroupBox("View Options", this);
    QVBoxLayout *viewLayout = new QVBoxLayout();
    
    viewLayout->addWidget(new QLabel("Visualization Type:"));
    viewTypeCombo = new QComboBox(this);
    viewTypeCombo->addItem("Contour Plot");
    viewTypeCombo->addItem("Vector Field");
    viewTypeCombo->addItem("Streamlines");
    viewTypeCombo->addItem("Isosurface");
    viewTypeCombo->addItem("Volume Rendering");
    viewLayout->addWidget(viewTypeCombo);
    
    viewGroup->setLayout(viewLayout);
    mainLayout->addWidget(viewGroup);
    
    mainLayout->addStretch();
    
    // Connect signals
    connect(paraViewButton, &QPushButton::clicked, this, &VisualizationWidget::launchParaView);
    connect(refreshButton, &QPushButton::clicked, this, &VisualizationWidget::refreshData);
    connect(timeStepCombo, QOverload<int>::of(&QComboBox::currentIndexChanged),
            this, &VisualizationWidget::selectTimeStep);
}

void VisualizationWidget::launchParaView()
{
    if (!caseManager->hasOpenCase()) {
        QMessageBox::warning(this, "No Case", "Please open or create a case first.");
        return;
    }
    
    caseManager->runParaFoam();
}

void VisualizationWidget::selectTimeStep(int index)
{
    // Update visualization for selected time step
    QString timeStep = timeStepCombo->itemText(index);
    updateFields();
}

void VisualizationWidget::selectField(int index)
{
    // Handle field selection
}

void VisualizationWidget::refreshData()
{
    if (!caseManager->hasOpenCase()) {
        return;
    }
    
    updateTimeSteps();
    updateFields();
}

void VisualizationWidget::updateTimeSteps()
{
    timeStepCombo->clear();
    
    // Scan case directory for time directories
    timeStepCombo->addItem("0");
    timeStepCombo->addItem("Latest");
}

void VisualizationWidget::updateFields()
{
    fieldList->clear();
    
    // Common OpenFOAM fields
    fieldList->addItem("U (Velocity)");
    fieldList->addItem("p (Pressure)");
    fieldList->addItem("T (Temperature)");
    fieldList->addItem("k (Turbulent Kinetic Energy)");
    fieldList->addItem("epsilon (Dissipation Rate)");
    fieldList->addItem("omega (Specific Dissipation Rate)");
}
