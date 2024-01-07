# frc2024

[![CI](https://github.com/sonic-howl/frc2024/actions/workflows/integrate.yml/badge.svg)](https://github.com/sonic-howl/frc2024/actions/workflows/integrate.yml)

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

### Installing WPILib 2024

To install the 2024 WPILib programming environment, follow [this guide](https://docs.wpilib.org/en/stable/docs/zero-to-robot/step-2/wpilib-setup.html).

If you're unsure of what options to choose during the install, follow these steps:

1. Click `start`
2. Select the `Everything` button, then press `Install for this User`
3. Select `Download for this computer only (fastest)`. Once finished, press `next`.
4. Click `Finish` to complete the install

> If you're using Mac or Linux, Make sure to read the `Post-Install` section.

This year, we will be programming in Java, so you can skip the C++ post installation steps.

Once installed, you'll have access to these tools:

- Visual Studio Code: The programming IDE (Integrated Development Environment
  )
- Gradle: Used to build the Java code
- Java JDK/JRE: The necessary version of Java
- WPILib Tools: Includes: SmartDashboard, Shuffleboard, RobotBuilder, Outline Viewer, Pathweaver, Glass, SysID
- WPILib Dependencies
- VS Code Extensions

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

## Configuring Hardware
In order to complete these steps, you will need to [intall the FRC Game Tools](#installing-frc-game-tools).

### RoboRIO Image Update

The frc 2024 season will require all RoboRIOs to be flashed with a new image. To update the RoboRIOs, please follow the [guide](https://docs.wpilib.org/en/stable/docs/zero-to-robot/step-3/index.html) depending on what version of RIO you have.

[**RoboRIO 2.0**](https://docs.wpilib.org/en/stable/docs/zero-to-robot/step-3/roborio2-imaging.html)

<img src="./static/roborio_2.png" width="400" height="400">

---

[**RoboRIO 1.0**](https://docs.wpilib.org/en/stable/docs/zero-to-robot/step-3/imaging-your-roborio.html)

<img src="./static/roborio_1.png" width="400" height="400">

### Programming the Radio

Similar to the RoboRIO, the radio used to communicate with the bot must also be flashed with the latest firmware. Follow [this guide](https://docs.wpilib.org/en/stable/docs/zero-to-robot/step-3/radio-programming.html) to do so.

## Build, Test, and Deploy
To view all available gradle commands, use the following command:

```bash
./gradlew tasks
```

Alternatively, you can view all available commands on the [docs](https://docs.wpilib.org/en/stable/docs/software/advanced-gradlerio/gradlew-tasks.html).

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

### Running the Robot Simulation

A robot simulation is available for testing. Read the full documentation [here](https://docs.wpilib.org/en/stable/docs/software/wpilib-tools/robot-simulation/introduction.html). 

You can run it with the following command:

```bash
./gradlew simulateJava
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