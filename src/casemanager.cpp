#include "casemanager.h"
#include <QFile>
#include <QTextStream>
#include <QProcess>
#include <QStandardPaths>

CaseManager::CaseManager(QObject *parent)
    : QObject(parent)
{
    m_processRunner = new ProcessRunner(this);
    
    connect(m_processRunner, &ProcessRunner::outputReceived,
            this, &CaseManager::logMessage);
    connect(m_processRunner, &ProcessRunner::errorReceived,
            this, &CaseManager::logMessage);
    connect(m_processRunner, &ProcessRunner::processFinished,
            this, [this](int exitCode) {
                emit logMessage("Process finished with code: " + QString::number(exitCode));
                emit processFinished("blockMesh", exitCode);
            });
}

CaseManager::~CaseManager()
{
}

bool CaseManager::createNewCase(const QString &path)
{
    m_casePath = path;
    
    if (!createCaseStructure()) {
        emit logMessage("ERROR: Failed to create case structure");
        return false;
    }
    
    emit caseOpened(path);
    emit logMessage("New case created successfully at: " + path);
    return true;
}

bool CaseManager::openCase(const QString &path)
{
    if (!validateCaseStructure(path)) {
        emit logMessage("ERROR: Invalid OpenFOAM case structure");
        return false;
    }
    
    m_casePath = path;
    emit caseOpened(path);
    emit logMessage("Case opened: " + path);
    return true;
}

bool CaseManager::saveCase()
{
    if (m_casePath.isEmpty()) {
        return false;
    }
    
    emit logMessage("Case saved");
    return true;
}

bool CaseManager::closeCase()
{
    if (m_casePath.isEmpty()) {
        return false;
    }
    
    m_casePath.clear();
    m_caseSettings.clear();
    emit caseClosed();
    emit logMessage("Case closed");
    return true;
}

QString CaseManager::currentCaseName() const
{
    if (m_casePath.isEmpty()) {
        return QString();
    }
    return QDir(m_casePath).dirName();
}

bool CaseManager::createCaseStructure()
{
    QDir caseDir(m_casePath);
    
    // Create standard OpenFOAM directories
    if (!caseDir.mkpath("0")) return false;
    if (!caseDir.mkpath("constant")) return false;
    if (!caseDir.mkpath("constant/polyMesh")) return false;
    if (!caseDir.mkpath("system")) return false;
    
    // Create basic dictionary files
    if (!createControlDict()) return false;
    if (!createFvSchemes()) return false;
    if (!createFvSolution()) return false;
    
    return true;
}

bool CaseManager::createControlDict()
{
    QFile file(m_casePath + "/system/controlDict");
    if (!file.open(QIODevice::WriteOnly | QIODevice::Text)) {
        return false;
    }
    
    QTextStream out(&file);
    out << "/*--------------------------------*- C++ -*----------------------------------*\\\n";
    out << "| =========                 |                                                 |\n";
    out << "| \\\\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |\n";
    out << "|  \\\\    /   O peration     | Version:  v2312                                 |\n";
    out << "|   \\\\  /    A nd           | Web:      www.OpenFOAM.org                      |\n";
    out << "|    \\\\/     M anipulation  |                                                 |\n";
    out << "\\*---------------------------------------------------------------------------*/\n";
    out << "FoamFile\n";
    out << "{\n";
    out << "    version     2.0;\n";
    out << "    format      ascii;\n";
    out << "    class       dictionary;\n";
    out << "    location    \"system\";\n";
    out << "    object      controlDict;\n";
    out << "}\n";
    out << "// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //\n\n";
    out << "application     icoFoam;\n\n";
    out << "startFrom       latestTime;\n\n";
    out << "startTime       0;\n\n";
    out << "stopAt          endTime;\n\n";
    out << "endTime         1;\n\n";
    out << "deltaT          0.01;\n\n";
    out << "writeControl    timeStep;\n\n";
    out << "writeInterval   10;\n\n";
    out << "purgeWrite      0;\n\n";
    out << "writeFormat     ascii;\n\n";
    out << "writePrecision  6;\n\n";
    out << "writeCompression off;\n\n";
    out << "timeFormat      general;\n\n";
    out << "timePrecision   6;\n\n";
    out << "runTimeModifiable true;\n\n";
    out << "// ************************************************************************* //\n";
    
    file.close();
    return true;
}

bool CaseManager::createFvSchemes()
{
    QFile file(m_casePath + "/system/fvSchemes");
    if (!file.open(QIODevice::WriteOnly | QIODevice::Text)) {
        return false;
    }
    
    QTextStream out(&file);
    out << "/*--------------------------------*- C++ -*----------------------------------*\\\n";
    out << "FoamFile\n";
    out << "{\n";
    out << "    version     2.0;\n";
    out << "    format      ascii;\n";
    out << "    class       dictionary;\n";
    out << "    location    \"system\";\n";
    out << "    object      fvSchemes;\n";
    out << "}\n";
    out << "// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //\n\n";
    out << "ddtSchemes\n";
    out << "{\n";
    out << "    default         Euler;\n";
    out << "}\n\n";
    out << "gradSchemes\n";
    out << "{\n";
    out << "    default         Gauss linear;\n";
    out << "}\n\n";
    out << "divSchemes\n";
    out << "{\n";
    out << "    default         none;\n";
    out << "}\n\n";
    out << "laplacianSchemes\n";
    out << "{\n";
    out << "    default         Gauss linear corrected;\n";
    out << "}\n\n";
    out << "interpolationSchemes\n";
    out << "{\n";
    out << "    default         linear;\n";
    out << "}\n\n";
    out << "snGradSchemes\n";
    out << "{\n";
    out << "    default         corrected;\n";
    out << "}\n\n";
    out << "// ************************************************************************* //\n";
    
    file.close();
    return true;
}

bool CaseManager::createFvSolution()
{
    QFile file(m_casePath + "/system/fvSolution");
    if (!file.open(QIODevice::WriteOnly | QIODevice::Text)) {
        return false;
    }
    
    QTextStream out(&file);
    out << "/*--------------------------------*- C++ -*----------------------------------*\\\n";
    out << "FoamFile\n";
    out << "{\n";
    out << "    version     2.0;\n";
    out << "    format      ascii;\n";
    out << "    class       dictionary;\n";
    out << "    location    \"system\";\n";
    out << "    object      fvSolution;\n";
    out << "}\n";
    out << "// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //\n\n";
    out << "solvers\n";
    out << "{\n";
    out << "    p\n";
    out << "    {\n";
    out << "        solver          PCG;\n";
    out << "        preconditioner  DIC;\n";
    out << "        tolerance       1e-06;\n";
    out << "        relTol          0.05;\n";
    out << "    }\n\n";
    out << "    pFinal\n";
    out << "    {\n";
    out << "        $p;\n";
    out << "        relTol          0;\n";
    out << "    }\n\n";
    out << "    U\n";
    out << "    {\n";
    out << "        solver          smoothSolver;\n";
    out << "        smoother        symGaussSeidel;\n";
    out << "        tolerance       1e-05;\n";
    out << "        relTol          0;\n";
    out << "    }\n";
    out << "}\n\n";
    out << "PISO\n";
    out << "{\n";
    out << "    nCorrectors     2;\n";
    out << "    nNonOrthogonalCorrectors 0;\n";
    out << "    pRefCell        0;\n";
    out << "    pRefValue       0;\n";
    out << "}\n\n";
    out << "// ************************************************************************* //\n";
    
    file.close();
    return true;
}

bool CaseManager::validateCaseStructure(const QString &path)
{
    QDir caseDir(path);
    
    // Check for essential directories
    if (!caseDir.exists("system")) return false;
    if (!caseDir.exists("constant")) return false;
    
    // Check for essential files
    if (!QFile::exists(path + "/system/controlDict")) return false;
    
    return true;
}

bool CaseManager::runBlockMesh()
{
    if (m_casePath.isEmpty()) {
        emit logMessage("ERROR: No case is open");
        return false;
    }
    
    emit processStarted("blockMesh");
    emit logMessage("Starting blockMesh in: " + m_casePath);
    
    // Run blockMesh through bash with OpenFOAM environment sourced
    QString command = "/bin/bash";
    QStringList arguments;
    QString fullCommand = "source /usr/lib/openfoam/openfoam2512/etc/bashrc && cd " + m_casePath + " && blockMesh";
    arguments << "-c" << fullCommand;
    
    emit logMessage("Executing: " + fullCommand);
    
    m_processRunner->runCommand(command, arguments, m_casePath);
    return true;
}

bool CaseManager::runSolver(const QString &solverName)
{
    if (m_casePath.isEmpty()) {
        emit logMessage("ERROR: No case is open");
        return false;
    }
    
    emit processStarted(solverName);
    emit logMessage("Starting solver: " + solverName + " in: " + m_casePath);
    
    // Run solver through bash with OpenFOAM environment sourced
    QString command = "/bin/bash";
    QStringList arguments;
    QString fullCommand = "source /usr/lib/openfoam/openfoam2512/etc/bashrc && cd " + m_casePath + " && " + solverName;
    arguments << "-c" << fullCommand;
    
    emit logMessage("Executing: " + fullCommand);
    m_processRunner->runCommand(command, arguments, m_casePath);
    
    return true;
}

bool CaseManager::runParaFoam()
{
    if (m_casePath.isEmpty()) {
        emit logMessage("ERROR: No case is open");
        return false;
    }
    
    emit processStarted("paraFoam");
    emit logMessage("Launching ParaView for mesh visualization...");
    
    // Create .foam file for ParaView to recognize the case
    QFileInfo caseInfo(m_casePath);
    QString caseName = caseInfo.fileName();
    QString foamFile = m_casePath + "/" + caseName + ".foam";
    
    // Touch the .foam file
    QFile file(foamFile);
    if (!file.exists()) {
        if (file.open(QIODevice::WriteOnly)) {
            file.close();
            emit logMessage("Created " + caseName + ".foam file");
        }
    }
    
    // Launch ParaView with the .foam file on display :1
    QString command = "/bin/bash";
    QStringList arguments;
    QString fullCommand = QString("source /usr/lib/openfoam/openfoam2512/etc/bashrc && "
                                 "cd %1 && "
                                 "DISPLAY=:1 paraview --data=%2.foam > /tmp/paraview.log 2>&1 &")
                                 .arg(m_casePath)
                                 .arg(caseName);
    arguments << "-c" << fullCommand;
    
    emit logMessage("Executing: " + fullCommand);
    m_processRunner->runCommand(command, arguments, m_casePath);
    emit logMessage("ParaView launched. Check the VNC browser window at http://localhost:6080/vnc_lite.html");
    
    return true;
}

bool CaseManager::runCheckMesh()
{
    if (m_casePath.isEmpty()) {
        emit logMessage("ERROR: No case is open");
        return false;
    }
    
    emit processStarted("checkMesh");
    emit logMessage("Running checkMesh to analyze mesh quality...");
    
    // Run checkMesh through bash with OpenFOAM environment sourced
    QString command = "/bin/bash";
    QStringList arguments;
    QString fullCommand = "source /usr/lib/openfoam/openfoam2512/etc/bashrc && cd " + m_casePath + " && checkMesh";
    arguments << "-c" << fullCommand;
    
    emit logMessage("Executing: " + fullCommand);
    
    m_processRunner->runCommand(command, arguments, m_casePath);
    return true;
}

QStringList CaseManager::getAvailableSolvers() const
{
    return QStringList() << "icoFoam" << "simpleFoam" << "pimpleFoam" 
                         << "interFoam" << "buoyantSimpleFoam";
}

QStringList CaseManager::getCaseFiles() const
{
    QStringList files;
    if (m_casePath.isEmpty()) {
        return files;
    }
    
    QDir caseDir(m_casePath);
    // Add logic to list case files
    
    return files;
}

void CaseManager::stopCurrentProcess()
{
    emit logMessage("Stopping current process...");
    // This will be implemented with ProcessRunner
}
