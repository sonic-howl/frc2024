# frc2024

| Branch  | Status                                                                                                                                                                         |
| ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| main    | [![CI](https://github.com/sonic-howl/frc2024/actions/workflows/integrate.yml/badge.svg?branch=main)](https://github.com/sonic-howl/frc2024/actions/workflows/integrate.yml)    |
| develop | [![CI](https://github.com/sonic-howl/frc2024/actions/workflows/integrate.yml/badge.svg?branch=develop)](https://github.com/sonic-howl/frc2024/actions/workflows/integrate.yml) |

## Getting started

### Installing FRC Game Tools

To install FRC's game tools for 2024, follow [this guide](https://docs.wpilib.org/en/stable/docs/zero-to-robot/step-2/frc-game-tools.html).

> Note: If you're on windows and you don't see the mount option after right clicking the iso file, you can open the file using `Open with` then `Windows Explorer`.
>
> ![Alt text](./static/mount-alternative.png)

Once installed, you'll have access to these tools:

- LabVIEW Update
- FRC Driver Station
- FRC roboRIO Imaging Tool and Images

### Installing WPILib 2024 (Python)

To install the 2024 WPILib programming environment for python, follow [this guide](https://docs.wpilib.org/en/stable/docs/zero-to-robot/step-2/python-setup.html).

If you're unsure of what options to choose during the install, follow these steps:

#### Installing Python

To get started, install python version 3.12.1 from these links and run the installer:

**[Windows](https://www.python.org/ftp/python/3.12.1/python-3.12.1-amd64.exe)**

> **Installation Steps**
>
> 1.  Select Modify
> 2.  Click Next
> 3.  Select `Associate files with Python` then click install

---

**[MacOS](https://www.python.org/ftp/python/3.12.1/python-3.12.1-macos11.pkg)**

#### Install VSCode

Follow the instructions [here](https://code.visualstudio.com/download) to install VSCode.

#### Extra Step on Windows

If you're on Windows, install this [Visual Studio package](https://aka.ms/vs/17/release/vc_redist.x64.exe) by downloading and running the installer.

#### Getting Started with VSCode

If you're new to VSCode, WPILib's docs have a good [starting guide](https://docs.wpilib.org/en/stable/docs/software/vscode-overview/vscode-basics.html#visual-studio-code-basics-and-the-wpilib-extension) explaining the basics.

### Cloning the GitHub Repository

In order to gain access to the robot code, clone the [Sonic Howl frc2024 repo](https://github.com/sonic-howl/frc2024).

If you don't know how to do this, follow these steps:

1. Open the repository [link](https://github.com/sonic-howl/frc2024) in your browser
2. Ask one of the organization admins to add you to the repo. (Neil, Nathan, Ramez). **TODO: Not sure if this is needed is repo is public. Update this section after testing.**
3. Click on the `Clone` button, choose HTTPS and copy the link to your clipboard.
4. Launch the `2024 WPILib VS Code` application.
5. Open the terminal by pressing the `CTRL + ~` keys.
6. Enter the command `git clone "the link you copied"`

> If you get an error mentioning that git isn't installed (or that no command named git exists), download it [here](https://git-scm.com/downloads).

### Installing RobotPy and Dependencies

Run the appropriate command in terminal depending on you operating system to install the project's dependencies.

**For Windows**

```bash
py -3 -m robotpy sync
```

**For Linux**

```bash
python3 -m robotpy sync
```

**For macOS**

```bash
python3 -m robotpy sync
```

## Configuring Hardware

In order to complete these steps, you will need to [install the FRC Game Tools](#installing-frc-game-tools).

### RoboRIO Image Update

The frc 2024 season will require all RoboRIOs to be flashed with a new image. To update the RoboRIOs, please follow the [guide](https://docs.wpilib.org/en/stable/docs/zero-to-robot/step-3/index.html) depending on what version of RIO you have.

[**RoboRIO 2.0**](https://docs.wpilib.org/en/stable/docs/zero-to-robot/step-3/roborio2-imaging.html)

<img src="./static/roborio_2.png" width="400" height="400">

---

[**RoboRIO 1.0**](https://docs.wpilib.org/en/stable/docs/zero-to-robot/step-3/imaging-your-roborio.html)

<img src="./static/roborio_1.png" width="400" height="400">

### Install RobotPY on RoboRIO

Follow [this guide](https://robotpy.readthedocs.io/en/stable/install/robot.html) to install python and RobotPY on the RobotRIO.

### Programming the Radio

Similar to the RoboRIO, the radio used to communicate with the bot must also be flashed with the latest firmware. Follow [this guide](https://docs.wpilib.org/en/stable/docs/zero-to-robot/step-3/radio-programming.html) to do so.

## Build and Deploy Commands

To view all available robotpy commands, use the following command:

```bash
# Linux
python3 -m robotpy

# Windows
py -3 -m robotpy
```

> You can pass the `--help` argument to see more information about the subcommand.
>
> For example, to see help for the sim command you can do the following:
>
> ```bash
> # Linux
> python3 -m robotpy sim --help
>
> # Windows
> py -3 -m robotpy sim --help
> ```

### Building Robot Code

Before deploying any robot code, you must build (compile) it first. To do so, you can follow [this guide](https://docs.wpilib.org/en/stable/docs/software/vscode-overview/deploying-robot-code.html#building-and-deploying-robot-code) (through ide) or run the following command:

```bash
./gradlew build
```

### Formatting Code

The following command can be used to format the code:

```bash
./gradlew spotlessApply
```

When code is pushed to the repository, a workflow will be run to check if the code is properly formatted. If it isn't, you won't be able to merge the code. In order to check if the project is properly formatted, run:

```bash
./gradlew spotlessCheck
```

### Using the Driver Station

This [guide](https://docs.wpilib.org/en/stable/docs/zero-to-robot/step-4/running-test-program.html) shows you how to setup the frc driver station in order to run your test programs.

### Deploying Code to Robot

After [building the code](#building-robot-code), you can deploy it to a connected robot using:

```bash
./gradlew deploy
```

If deploying wirelessly, you can scan for robot IP's using:

```bash
./gradlew discoverRoborio
```

## Simulation Testing

WPILib provides a [simulator](https://docs.wpilib.org/en/stable/docs/software/wpilib-tools/robot-simulation/introduction.html) to test your code without being physically connected to a robot.

### Running the Robot Simulation

A robot simulation is available for testing. Read the full documentation [here](https://docs.wpilib.org/en/stable/docs/software/wpilib-tools/robot-simulation/introduction.html).

You can run it with the following command:

```bash
./gradlew simulateJava
```

> It's important to note that robot simulation is only enabled when `includeDesktopSupport` is set to true in `build.gradle`. When enabled, this option can cause issues with 3rd party software that doesn't support it. If ever you run into build or simulation issues, try turning off that option in the build file. You can also follow [this guide](https://docs.wpilib.org/en/stable/docs/software/wpilib-tools/robot-simulation/simulation-gui.html#determining-simulation-from-robot-code) in order to conditionally run certain code based on the environment (if the simulation if running or not).

### Running Robot Dashboards during a Simulation

Follow [this guide](https://docs.wpilib.org/en/stable/docs/software/wpilib-tools/robot-simulation/introduction.html#running-robot-dashboards) to enable whichever dashboard you plan on using during the simulation.

### Run Tests

You can also manually run unit tests using:

```bash
./gradlew test
```
