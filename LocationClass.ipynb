{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": []
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "code",
      "source": [
        "#Libraries\n",
        "import threading\n",
        "#import random\n",
        "#import time"
      ],
      "metadata": {
        "id": "ZyGZbi0H1oHd"
      },
      "execution_count": 8,
      "outputs": []
    },
    {
      "cell_type": "code",
      "execution_count": 21,
      "metadata": {
        "id": "hAqVzbYJ1lWA"
      },
      "outputs": [],
      "source": [
        "#Location class\n",
        "\n",
        "class Location:\n",
        "  def __init__(self):\n",
        "    #Here go the lists and locks of the location\n",
        "    #Pay attention to the structure. The dictionary makes adding or removing new lists easier\n",
        "    #Wasted, drugged, etc will be referred to as 'states'\n",
        "    self.neighbours=[]\n",
        "    self.states={\n",
        "        'all':{'list':[], 'lock':threading.Lock()},\n",
        "        'wasted':{'list':[], 'lock':threading.Lock()},\n",
        "        'drugged':{'list':[], 'lock':threading.Lock()},\n",
        "        'fighting':{'list':[], 'lock':threading.Lock()}\n",
        "    }\n",
        "\n",
        "  def addState(self, spectator, state):\n",
        "    #Give a spectator a state\n",
        "    #Returns True if the spectator is still at location, False if not, None if there was an error\n",
        "    #Same holds for other methods\n",
        "    if state in self.states.keys():\n",
        "      with self.states['all']['lock']:\n",
        "        if spectator not in self.states['all']['list']:\n",
        "          #Keep in mind return breaks out of the function\n",
        "          return False\n",
        "      with self.states[state]['lock']:\n",
        "        self.states[state]['list'].append(spectator)\n",
        "        return True\n",
        "    else:\n",
        "      print(f\"State {state} was requested but doesn't exist\")\n",
        "      return None\n",
        "\n",
        "  def removeState(self, spectator, state):\n",
        "    #Remove a spectator's state\n",
        "    if state in self.states.keys():\n",
        "      with self.states[state]['lock']:\n",
        "        if spectator not in self.states[state]['list']:\n",
        "          return False\n",
        "        else:\n",
        "          self.states[state]['list'].remove(spectator)\n",
        "          return True\n",
        "    else:\n",
        "      print(f\"State {state} was requested but doesn't exist\")\n",
        "      return None\n",
        "\n",
        "  def checkStates(self, spectator):\n",
        "    #Returns a list of all states of an spectator\n",
        "    #Removed spectator in 'all' check\n",
        "    #Should 'all' be returned?\n",
        "    #Might need revision\n",
        "    states=[]\n",
        "    for state in self.states.keys():\n",
        "      if state=='all':\n",
        "        continue\n",
        "      with self.states[state]['lock']:\n",
        "        if spectator in self.states[state]['list']:\n",
        "          states.append(state)\n",
        "    return states\n",
        "\n",
        "  def getStateList(self, state='all'):\n",
        "    #Returns the list of all spectators that have a specific state\n",
        "    if state not in self.states.keys():\n",
        "      print(f\"State {state} was requested but doesn't exist\")\n",
        "      return None\n",
        "    else:\n",
        "      with self.states[state]['lock']:\n",
        "        return self.states[state]['list']\n",
        "\n",
        "  def sendTo(self, spectator, target):\n",
        "    #Sends an spectator to a neighbour location\n",
        "    #Does it need to be a neighbour?\n",
        "    with self.states['all']['lock']:\n",
        "      if spectator not in self.states['all']['list']:\n",
        "        return False\n",
        "      else:\n",
        "        states=self.checkStates(spectator)\n",
        "        for state in states:\n",
        "          self.removeState(spectator, state)\n",
        "        target.receive(spectator, states)\n",
        "        return True\n",
        "\n",
        "  def receive(self, spectator, states=[]):\n",
        "    #Receives an spectator from another location\n",
        "    states = ['all'] + states\n",
        "    for state in states:\n",
        "      if state in self.states.keys():\n",
        "        with self.states[state]['lock']:\n",
        "          self.states[state]['list'].append(spectator)\n",
        ""
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "#Examples of the Location class in action\n",
        "\n",
        "stage1=Location()\n",
        "stage1.receive('John')\n",
        "stage1.receive('Peter')\n",
        "print(stage1.getStateList())\n",
        "\n",
        "stage1.addState('John', 'wasted')\n",
        "print(stage1.getStateList('wasted'))\n",
        "print(stage1.checkStates('John'))\n",
        "\n",
        "stage1.removeState('John', 'wasted')\n",
        "print(stage1.getStateList('wasted'))\n",
        "print(stage1.checkStates('John'))\n",
        "\n",
        "stage2=Location()\n",
        "stage2.receive('Mary')\n",
        "stage2.addState('Mary', 'wasted')\n",
        "stage2.sendTo('Mary', stage1)\n",
        "print(stage1.getStateList('wasted'))\n",
        "print(stage1.checkStates('Mary'))"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "4XV6QBXADhdL",
        "outputId": "47a73ca0-e8b7-450b-ee55-7240f91d3180"
      },
      "execution_count": 22,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "['John', 'Peter']\n",
            "['John']\n",
            "['wasted']\n",
            "[]\n",
            "[]\n",
            "['Mary']\n",
            "['wasted']\n"
          ]
        }
      ]
    }
  ]
}