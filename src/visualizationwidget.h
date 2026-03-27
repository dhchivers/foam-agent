#ifndef VISUALIZATIONWIDGET_H
#define VISUALIZATIONWIDGET_H

#include <QWidget>
#include <QPushButton>
#include <QComboBox>
#include <QGroupBox>
#include <QListWidget>
#include "casemanager.h"

class VisualizationWidget : public QWidget
{
    Q_OBJECT

public:
    explicit VisualizationWidget(CaseManager *manager, QWidget *parent = nullptr);
    ~VisualizationWidget();

private slots:
    void launchParaView();
    void selectTimeStep(int index);
    void selectField(int index);
    void refreshData();

private:
    void setupUI();
    void updateTimeSteps();
    void updateFields();
    
    CaseManager *caseManager;
    
    QGroupBox *controlGroup;
    QPushButton *paraViewButton;
    QPushButton *refreshButton;
    
    QGroupBox *dataGroup;
    QComboBox *timeStepCombo;
    QListWidget *fieldList;
    
    QGroupBox *viewGroup;
    QComboBox *viewTypeCombo;
};

#endif // VISUALIZATIONWIDGET_H
