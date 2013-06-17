# Copyright (c) 2012 Santosh Philip

# This file is part of eppy.

# Eppy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Eppy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with eppy.  If not, see <http://www.gnu.org/licenses/>.

"""py.test for hvacbuilder"""
import sys
import os
sys.path.append('../')
import hvacbuilder
from modeleditor import IDF
import random
from StringIO import StringIO

# idd is read only once in this test
from iddcurrent import iddcurrent
iddfhandle = StringIO(iddcurrent.iddtxt)
IDF.setiddname(iddfhandle)


def test_flattencopy():
    """py.test for flattencopy"""
    tdata = (([1,2], [1,2]), #lst , nlst
    ([1,2,[3,4]], [1,2,3,4]), #lst , nlst
    ([1,2,[3,[4,5,6],7,8]], [1,2,3,4,5,6,7,8]), #lst , nlst
    ([1,2,[3,[4,5,[6,7],8],9]], [1,2,3,4,5,6,7,8,9]), #lst , nlst
    )
    for lst , nlst in tdata:
        result = hvacbuilder.flattencopy(lst)
        assert result == nlst

def test_makeplantloop():
    """pytest for makeplantloop"""
    tdata = (("", 
    "p_loop",
    ['sb0', ['sb1', 'sb2', 'sb3'], 'sb4'],
    ['db0', ['db1', 'db2', 'db3'], 'db4'],
    """BRANCH, sb0, 0, , Pipe:Adiabatic, sb0_pipe, p_loop Supply Inlet, sb0_pipe_outlet, Bypass;BRANCH, sb1, 0, , Pipe:Adiabatic, sb1_pipe, sb1_pipe_inlet, sb1_pipe_outlet, Bypass;BRANCH, sb2, 0, , Pipe:Adiabatic, sb2_pipe, sb2_pipe_inlet, sb2_pipe_outlet, Bypass;BRANCH, sb3, 0, , Pipe:Adiabatic, sb3_pipe, sb3_pipe_inlet, sb3_pipe_outlet, Bypass;BRANCH, sb4, 0, , Pipe:Adiabatic, sb4_pipe, sb4_pipe_inlet, p_loop Supply Outlet, Bypass;BRANCH, db0, 0, , Pipe:Adiabatic, db0_pipe, p_loop Demand Inlet, db0_pipe_outlet, Bypass;BRANCH, db1, 0, , Pipe:Adiabatic, db1_pipe, db1_pipe_inlet, db1_pipe_outlet, Bypass;BRANCH, db2, 0, , Pipe:Adiabatic, db2_pipe, db2_pipe_inlet, db2_pipe_outlet, Bypass;BRANCH, db3, 0, , Pipe:Adiabatic, db3_pipe, db3_pipe_inlet, db3_pipe_outlet, Bypass;BRANCH, db4, 0, , Pipe:Adiabatic, db4_pipe, db4_pipe_inlet, p_loop Demand Outlet, Bypass;BRANCHLIST, p_loop Supply Branchs, sb1, sb2, sb3;BRANCHLIST, p_loop Demand Branchs, db1, db2, db3;CONNECTOR:SPLITTER, p_loop_supply_splitter, sb0, sb1, sb2, sb3;CONNECTOR:SPLITTER, p_loop_demand_splitter, db0, db1, db2, db3;CONNECTOR:MIXER, p_loop_supply_mixer, sb4, sb1, sb2, sb3;CONNECTOR:MIXER, p_loop_demand_mixer, db4, db1, db2, db3;CONNECTORLIST, p_loop Supply Connectors, Connector:Splitter, p_loop_supply_splitter, Connector:Mixer, p_loop_supply_mixer;CONNECTORLIST, p_loop Demand Connectors, Connector:Splitter, p_loop_demand_splitter, Connector:Mixer, p_loop_demand_mixer;PIPE:ADIABATIC, sb0_pipe, p_loop Supply Inlet, sb0_pipe_outlet;PIPE:ADIABATIC, sb1_pipe, sb1_pipe_inlet, sb1_pipe_outlet;PIPE:ADIABATIC, sb2_pipe, sb2_pipe_inlet, sb2_pipe_outlet;PIPE:ADIABATIC, sb3_pipe, sb3_pipe_inlet, sb3_pipe_outlet;PIPE:ADIABATIC, sb4_pipe, sb4_pipe_inlet, p_loop Supply Outlet;PIPE:ADIABATIC, db0_pipe, p_loop Demand Inlet, db0_pipe_outlet;PIPE:ADIABATIC, db1_pipe, db1_pipe_inlet, db1_pipe_outlet;PIPE:ADIABATIC, db2_pipe, db2_pipe_inlet, db2_pipe_outlet;PIPE:ADIABATIC, db3_pipe, db3_pipe_inlet, db3_pipe_outlet;PIPE:ADIABATIC, db4_pipe, db4_pipe_inlet, p_loop Demand Outlet;PLANTLOOP, p_loop, Water, , , , , , , 0.0, Autocalculate, p_loop Supply Inlet, p_loop Supply Outlet, p_loop Supply Branchs, p_loop Supply Connectors, p_loop Demand Inlet, p_loop Demand Outlet, p_loop Demand Branchs, p_loop Demand Connectors, Sequential, , SingleSetpoint, None, None;"""
    ), # blankidf, loopname, sloop, dloop, nidf
    )
    for blankidf, loopname, sloop, dloop, nidf in tdata:
        
        fhandle = StringIO("")
        idf1 = IDF(fhandle)
        loopname = "p_loop"
        sloop = ['sb0', ['sb1', 'sb2', 'sb3'], 'sb4']
        dloop = ['db0', ['db1', 'db2', 'db3'], 'db4']
        hvacbuilder.makeplantloop(idf1, loopname, sloop, dloop)
        idf2 = IDF(StringIO(nidf))
        assert str(idf1.model) == str(idf2.model)

def test_getbranchcomponents():
    """py.test for getbranchcomponents"""
    tdata = (
    ("""BRANCH,
     sb1,
     0,
     ,
     PIPE:ADIABATIC,
     np1,
     np1_inlet,
     np1_np2_node,
     ,
     PIPE:ADIABATIC,
     np2,
     np1_np2_node,
     np2_outlet,
     ;
""", 
    True, 
    [('PIPE:ADIABATIC', 'np1'), 
    ('PIPE:ADIABATIC', 'np2')]), # idftxt, utest, componentlist
    ("""BRANCH,
     sb1,
     0,
     ,
     PIPE:ADIABATIC,
     np1,
     np1_inlet,
     np1_np2_node,
     ,
     PIPE:ADIABATIC,
     np2,
     np1_np2_node,
     np2_outlet,
     ;
PIPE:ADIABATIC,
     np1,
     np1_inlet,
     np1_np2_node;

PIPE:ADIABATIC,
     np2,
     np1_np2_node,
     np2_outlet;

""", 
    False, 
    [['PIPE:ADIABATIC', 'np1', 'np1_inlet', 'np1_np2_node'], 
    ['PIPE:ADIABATIC', 'np2', 'np1_np2_node', 'np2_outlet']]), # idftxt, utest, componentlist
    )
    for idftxt, utest, componentlist in tdata:
        fhandle = StringIO(idftxt)
        idf = IDF(fhandle)
        branch = idf.idfobjects['BRANCH'][0]
        result = hvacbuilder.getbranchcomponents(idf, branch, utest=utest)
        if utest:
            assert result == componentlist
        else:
            lresult =[item.obj for item in result]
            assert lresult == componentlist
            
def test_renamenodes():
    """py.test for renamenodes"""
    idftxt = """PIPE:ADIABATIC,
         np1,
         np1_inlet,
         np1_outlet;
         !- ['np1_outlet', 'np1_np2_node'];

    BRANCH,
         sb0,
         0,
         ,
         Pipe:Adiabatic,
         np1,
         np1_inlet,
         np1_outlet,
         Bypass;
    """
    outtxt = """PIPE:ADIABATIC,
         np1,
         np1_inlet,
         np1_np2_node;
         !- ['np1_outlet', 'np1_np2_node'];

    BRANCH,
         sb0,
         0,
         ,
         Pipe:Adiabatic,
         np1,
         np1_inlet,
         np1_np2_node,
         Bypass;
    """
    # !- ['np1_outlet', 'np1_np2_node'];
    fhandle = StringIO(idftxt)
    idf = IDF(fhandle)
    pipe = idf.idfobjects['PIPE:ADIABATIC'][0]
    pipe.Outlet_Node_Name = ['np1_outlet', 'np1_np2_node'] # this is the first step of the replace
    hvacbuilder.renamenodes(idf, fieldtype='node')
    outidf = IDF(StringIO(outtxt))
    result = idf.idfobjects['PIPE:ADIABATIC'][0].obj
    print result 
    print outidf.idfobjects['PIPE:ADIABATIC'][0].obj 
    assert result == outidf.idfobjects['PIPE:ADIABATIC'][0].obj 

def test_getfieldnamesendswith():
    """py.test for getfieldnamesendswith"""
    idftxt = """PIPE:ADIABATIC,           
        np2,                      !- Name
        np1_np2_node,             !- Inlet Node Name
        np2_outlet;               !- Outlet Node Name

    """
    tdata = (("Inlet_Node_Name",["Inlet_Node_Name"]), # endswith, fieldnames
    ("Node_Name",["Inlet_Node_Name", 
                "Outlet_Node_Name"]), # endswith, fieldnames
    ("Name",["Name",
                "Inlet_Node_Name", 
                "Outlet_Node_Name"]), # endswith, fieldnames
    )    
    fhandle = StringIO(idftxt)
    idf = IDF(fhandle)
    idfobject = idf.idfobjects["PIPE:ADIABATIC"][0]
    for endswith, fieldnames in tdata:
        result = hvacbuilder.getfieldnamesendswith(idfobject, endswith)
        assert result == fieldnames
        
def test_connectcomponents():
    """py.test for connectcomponents"""
    fhandle = StringIO("")
    idf = IDF(fhandle)
    
    tdata = ((
    [idf.newidfobject("PIPE:ADIABATIC", "pipe1"),
    idf.newidfobject("PIPE:ADIABATIC", "pipe2")],
    ["pipe1_Inlet_Node_Name", ["pipe2_Inlet_Node_Name", "pipe1_pipe2_node"]],
    [["pipe1_Outlet_Node_Name", "pipe1_pipe2_node"], 
                                                "pipe2_Outlet_Node_Name"],
    '' ), 
    (
    [idf.newidfobject("Coil:Cooling:Water".upper(), "pipe1"),
    idf.newidfobject("Coil:Cooling:Water".upper(), "pipe2")],
    ['pipe1_Water_Inlet_Node_Name', 'pipe1_Air_Inlet_Node_Name', 
        'pipe2_Water_Inlet_Node_Name',
        ['pipe2_Air_Inlet_Node_Name', 'pipe1_pipe2_node']],
    ['pipe1_Water_Outlet_Node_Name', ['pipe1_Air_Outlet_Node_Name', 
        'pipe1_pipe2_node'], 'pipe2_Water_Outlet_Node_Name', 
        'pipe2_Air_Outlet_Node_Name'],
    'Air' ), 
    # components, inlets, outlets, fluid
    )
    for components, inlets, outlets, fluid in tdata:
        # init the nodes in the new components
        for component in components:
            hvacbuilder.initinletoutlet(idf, component)
        hvacbuilder.connectcomponents(idf, components, fluid)
        inresult = []
        for component in components:
            fldnames = hvacbuilder.getfieldnamesendswith(component, 
                                                    "Inlet_Node_Name")
            for name in fldnames:
                inresult.append(component[name])
        assert inresult == inlets
        outresult = []
        for component in components:
            fldnames = hvacbuilder.getfieldnamesendswith(component, 
                                                    "Outlet_Node_Name")
            for name in fldnames:
                outresult.append(component[name])
        assert outresult == outlets
            
    
def test_initinletoutlet():
    """py.test for initinletoutlet"""
    tdata = (
    ('PIPE:ADIABATIC', 
    'apipe', 
    True,
    ["apipe_Inlet_Node_Name"], 
    ["apipe_Outlet_Node_Name"]), # idfobjectkey, idfobjname, inlets, outlets
    ('Coil:Cooling:Water'.upper(), 
    'acoil', 
    True,
    ["acoil_Water_Inlet_Node_Name", "acoil_Air_Inlet_Node_Name"], 
    ["acoil_Water_Outlet_Node_Name", "acoil_Air_Outlet_Node_Name"]), 
    # idfobjectkey, idfobjname, force, inlets, outlets
    ('PIPE:ADIABATIC', 
    'apipe', 
    False,
    ["Gumby"], 
    ["apipe_Outlet_Node_Name"]), # idfobjectkey, idfobjname, inlets, outlets
    ) 
    fhandle = StringIO("")
    idf = IDF(fhandle)
    for idfobjectkey, idfobjname, force, inlets, outlets in tdata:
        idfobject = idf.newidfobject(idfobjectkey, idfobjname)
        inodefields = hvacbuilder.getfieldnamesendswith(idfobject, 
                                                "Inlet_Node_Name")
        idfobject[inodefields[0]] = "Gumby"
        hvacbuilder.initinletoutlet(idf, idfobject, force)
        inodefields = hvacbuilder.getfieldnamesendswith(idfobject, 
                                                "Inlet_Node_Name")
        for nodefield, inlet in zip(inodefields, inlets):
            result = idfobject[nodefield]
            assert result == inlet
        onodefields = hvacbuilder.getfieldnamesendswith(idfobject, 
                                                "Outlet_Node_Name")
        for nodefield, outlet in zip(onodefields, outlets):
            result = idfobject[nodefield]
            assert result == outlet

def test_componentsintobranch():
    """py.test for componentsintobranch"""
    tdata = (
    ("""BRANCH,
         sb0,
         0,
         ,
         Pipe:Adiabatic,
         sb0_pipe,
         p_loop Supply Inlet,
         sb0_pipe_outlet,
         Bypass;
    """, 
    [("PIPE:ADIABATIC", "pipe1"), ("PIPE:ADIABATIC", "pipe1")],
    '',
    []), 
    # idftxt, complst, fluid, branchcomps
    )                                                    
    for idftxt, complst, fluid, branchcomps in tdata:
        fhandle = StringIO(idftxt)
        idf = IDF(fhandle)
        components = [idf.newidfobject(key, nm) for key, nm in complst]
        branch = idf.idfobjects['BRANCH'][0]
        branch = hvacbuilder.componentsintobranch(idf, branch, components, 
                                                                    fluid)
        print branch.obj[4:]
        print branchcomps
        assert branch.obj[4:] == branchcomps
        