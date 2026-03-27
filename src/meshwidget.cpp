#include "meshwidget.h"
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QGridLayout>
#include <QLabel>
#include <QMessageBox>

MeshWidget::MeshWidget(CaseManager *manager, QWidget *parent)
    : QWidget(parent), caseManager(manager)
{
    setupUI();
}

MeshWidget::~MeshWidget()
{
}

void MeshWidget::setupUI()
{
    QVBoxLayout *mainLayout = new QVBoxLayout(this);
    
    // Mesh type selection
    meshTypeGroup = new QGroupBox("Mesh Generation Method", this);
    QVBoxLayout *typeLayout = new QVBoxLayout();
    
    meshTypeCombo = new QComboBox(this);
    meshTypeCombo->addItem("blockMesh - Structured Mesh");
    meshTypeCombo->addItem("snappyHexMesh - Complex Geometry");
    meshTypeCombo->addItem("Import External Mesh");
    typeLayout->addWidget(meshTypeCombo);
    
    QHBoxLayout *buttonLayout = new QHBoxLayout();
    blockMeshButton = new QPushButton("Run blockMesh", this);
    snappyButton = new QPushButton("Run snappyHexMesh", this);
    checkQualityButton = new QPushButton("Check Quality", this);
    importButton = new QPushButton("Import Mesh", this);
    
    buttonLayout->addWidget(blockMeshButton);
    buttonLayout->addWidget(snappyButton);
    buttonLayout->addWidget(checkQualityButton);
    buttonLayout->addWidget(importButton);
    typeLayout->addLayout(buttonLayout);
    
    meshTypeGroup->setLayout(typeLayout);
    mainLayout->addWidget(meshTypeGroup);
    
    // Mesh parameters
    meshParamsGroup = new QGroupBox("Mesh Parameters (blockMesh)", this);
    QGridLayout *paramsLayout = new QGridLayout();
    
    paramsLayout->addWidget(new QLabel("Cells in X:"), 0, 0);
    cellsXSpin = new QSpinBox(this);
    cellsXSpin->setRange(1, 1000);
    cellsXSpin->setValue(20);
    paramsLayout->addWidget(cellsXSpin, 0, 1);
    
    paramsLayout->addWidget(new QLabel("Cells in Y:"), 1, 0);
    cellsYSpin = new QSpinBox(this);
    cellsYSpin->setRange(1, 1000);
    cellsYSpin->setValue(20);
    paramsLayout->addWidget(cellsYSpin, 1, 1);
    
    paramsLayout->addWidget(new QLabel("Cells in Z:"), 2, 0);
    cellsZSpin = new QSpinBox(this);
    cellsZSpin->setRange(1, 1000);
    cellsZSpin->setValue(20);
    paramsLayout->addWidget(cellsZSpin, 2, 1);
    
    meshParamsGroup->setLayout(paramsLayout);
    mainLayout->addWidget(meshParamsGroup);
    
    // Mesh log output
    QLabel *logLabel = new QLabel("Mesh Generation Log:", this);
    mainLayout->addWidget(logLabel);
    
    meshLogText = new QTextEdit(this);
    meshLogText->setReadOnly(true);
    mainLayout->addWidget(meshLogText);
    
    // Connect signals
    connect(blockMeshButton, &QPushButton::clicked, this, &MeshWidget::runBlockMesh);
    connect(snappyButton, &QPushButton::clicked, this, &MeshWidget::runSnappyHexMesh);
    connect(checkQualityButton, &QPushButton::clicked, this, &MeshWidget::checkMeshQuality);
    connect(importButton, &QPushButton::clicked, this, &MeshWidget::importMesh);
    
    // Connect to CaseManager log messages
    connect(caseManager, &CaseManager::logMessage, this, &MeshWidget::appendLog);
}

void MeshWidget::runBlockMesh()
{
    if (!caseManager->hasOpenCase()) {
        QMessageBox::warning(this, "No Case", "Please open or create a case first.");
        return;
    }
    
    meshLogText->append("Starting blockMesh generation...");
    caseManager->runBlockMesh();
}

void MeshWidget::runSnappyHexMesh()
{
    if (!caseManager->hasOpenCase()) {
        QMessageBox::warning(this, "No Case", "Please open or create a case first.");
        return;
    }
    
    meshLogText->append("Starting snappyHexMesh...");
    // Implementation in ProcessRunner
}

void MeshWidget::checkMeshQuality()
{
    if (!caseManager->hasOpenCase()) {
        QMessageBox::warning(this, "No Case", "Please open or create a case first.");
        return;
    }
    
    meshLogText->append("Checking mesh quality...");
    // Run checkMesh command
}

void MeshWidget::importMesh()
{
    if (!caseManager->hasOpenCase()) {
        QMessageBox::warning(this, "No Case", "Please open or create a case first.");
        return;
    }
    
    meshLogText->append("Import mesh functionality coming soon...");
    // Implementation for mesh import
}

void MeshWidget::appendLog(const QString &message)
{
    meshLogText->append(message);
}
