#ifndef MESHWIDGET_H
#define MESHWIDGET_H

#include <QWidget>
#include <QPushButton>
#include <QTextEdit>
#include <QGroupBox>
#include <QComboBox>
#include <QSpinBox>
#include "casemanager.h"

class MeshWidget : public QWidget
{
    Q_OBJECT

public:
    explicit MeshWidget(CaseManager *manager, QWidget *parent = nullptr);
    ~MeshWidget();

private slots:
    void runBlockMesh();
    void runSnappyHexMesh();
    void checkMeshQuality();
    void importMesh();
    void appendLog(const QString &message);

private:
    void setupUI();
    
    CaseManager *caseManager;
    
    QGroupBox *meshTypeGroup;
    QComboBox *meshTypeCombo;
    QPushButton *blockMeshButton;
    QPushButton *snappyButton;
    QPushButton *checkQualityButton;
    QPushButton *importButton;
    
    QGroupBox *meshParamsGroup;
    QSpinBox *cellsXSpin;
    QSpinBox *cellsYSpin;
    QSpinBox *cellsZSpin;
    
    QTextEdit *meshLogText;
};

#endif // MESHWIDGET_H
