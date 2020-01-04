# -*- coding: utf-8 -*-
"""
Created on Mon Dec 23 15:07:00 2019

@author: c.camilli
"""

from threading import Thread
import time

def parse_input(path):
    with open(path) as file:
        l = [int(v.rstrip('\n')) for v in file.read().split(',')]
    return l

code = parse_input('..\\inputs\\23.in')
#%%

class IntCode():
    def __init__(self, code, inputs):
        self._state = code.copy()
        self._header, self.ninputs, self._relative_base = 0, 0, 0
        self._hOps = {1:lambda x, y: x+y, 2:lambda x, y: x*y}        
        self._verbose = False
        self._input = inputs
        
    def _solve_op_and_modes(self):
        opcode, modes = self._parse_instr()
        return opcode, [self._parse_modes(el) for el in modes]
            
    def _treat_op_modes(self, op, modes):
        if op in [1, 2]:
            modes[2](3, "update", self._hOps[op](modes[0](1), modes[1](2)))
        elif op == 3:
            modes[0](1, "update", self._input[self.ninputs])
            self._log(f"Wrote {self._input[self.ninputs]} to position {modes[0](1)}")
            self.ninputs += 1
        elif op == 4:
            self._output = modes[0](1)
            self._log(f"Output was set to {modes[0](1)}")
        elif op == 5:
            if modes[0](1) != 0:
                self._header = modes[1](2)
            else:
                self._header += 3
        elif op == 6:
            if modes[0](1) == 0:
                self._header = modes[1](2)
            else:
                self._header += 3
        elif op == 7:
            if modes[0](1) < modes[1](2):
                modes[2](3, "update", 1)
            else:
                modes[2](3, "update", 0)                
        elif op == 8:
            if modes[0](1) == modes[1](2):
                modes[2](3, "update", 1)
            else:
                modes[2](3, "update", 0)               
        elif op == 9:
            self._relative_base += modes[0](1)
                
    def _parse_instr(self):
        v = self._fetch1(0)
        self._log(f"Brute instruction is {v}")
        return v%100, [v//100%10, v//1000%10, v//10000%10]
                       
    def _parse_modes(self, var):
        if var == 0:
            return self._fetch0
        elif var == 1:
            return self._fetch1
        elif var == 2:
            return self._fetch2    
                                                           
    def _fetch0(self, offset, mode='regular', update_arg=0):
        if mode == 'regular':
            return self._state[self._state[self._header + offset]]
        else:
            self._state[self._state[self._header + offset]] = update_arg
    
    def _fetch1(self, offset, mode='regular', update_arg=0):
        if mode == 'regular':
            return self._state[self._header + offset]
        else:
            self._state[self._header + offset] = update_arg
    
    def _fetch2(self, offset, mode='regular', update_arg=0):
        if mode == 'regular':
            return self._state[self._state[self._header + offset] + self._relative_base]
        else:
            self._state[self._state[self._header + offset] + self._relative_base] = update_arg         
    
    def _update(self, op):
        if op in [1, 2, 7, 8]:
            self._header += 4
        elif op in [3, 4, 9]:
            self._header += 2
        self._log(f"Updated header to {self._header}")
    
    def _log(self, msg):
       if not self._verbose:
            pass
       else:
            print(msg)

    def _run_instructions_and_update(self, op, modes):
        self._log(f"Operation code is {self._fetch1(0)}")
        self._treat_op_modes(op, modes)
        self._update(op)
        return self._solve_op_and_modes()
    
    def _extend_memory(self, a):
        if (a<0):
            raise ValueError("Trying to access negative memory")
        else:
            while len(self._state) <= a:
                self._state.append(0)
        
    def run(self, verbose=False):
        self._verbose = verbose
        op, modes = self._solve_op_and_modes()
        while op != 99:
            if op == 4:
                op, modes = self._run_instructions_and_update(op, modes)
                yield self._output
            elif op == 3:
                yield "Please provide input"
                op, modes = self._run_instructions_and_update(op, modes)
            else:
                op, modes = self._run_instructions_and_update(op, modes)
        
    
    def run_fbl(self, verbose=False):
        self._verbose = verbose
        op, modes = self._solve_op_and_modes()
        while op not in [99, 4]:
            op, modes = self._run_instructions_and_update(op, modes)
        if op == 4:
            op, modes = self._run_instructions_and_update(op, modes)
        return (op == 99), self._output
    

class Packet():
    
    def __init__(self, destination, x, y):
        self.destination = destination
        self.x = x
        self.y = y

packet_queue = {}
tried_to_receive = 0
packages_sent = 0

class NetworkNode(Thread):
    
    def __init__(self, nic_code, net_address):
        super().__init__()
        self.computer = IntCode(nic_code + [0]*10000, [])
        self.id = net_address
        self.input_queue = [net_address]
        self.input_pointer = 0
        self.output_queue = []
        self.output_pointer = 0
        self.packets_fetched = 0
        
    def run(self):
        gen = self.computer.run()
        try:
            while True:
                out = next(gen)
                if out == 'Please provide input':
                    inp = self.fetch_input()
                    self.computer._input.append(inp)
                else:
                    self.process_output(out)
        except StopIteration:
            print(f"Node {self.id} finished running")
                    
    def fetch_input(self):
        global tried_to_receive
        self.fetch_packets()
        if self.input_pointer == len(self.input_queue):
            tried_to_receive += 1
            return -1
        else:
            val = self.input_queue[self.input_pointer]
            self.input_pointer += 1
            return val
        
    def process_output(self, out):
        self.output_queue.append(out)
        self.output_pointer += 1
        if self.output_pointer > 0 and self.output_pointer % 3 == 0:
            self.send_packet(Packet(*self.output_queue[(self.output_pointer-3):self.output_pointer]))
            
    def send_packet(self, packet):
        global packages_sent
        if packet.destination not in packet_queue:
            packet_queue[packet.destination] = []
            if packet.destination == 255:
                print(f"Answer for part 1 is {packet.y}")
        packet_queue[packet.destination].append((packet.x, packet.y))
        if packet.destination != 255:
            packages_sent += 1
            
    def fetch_packets(self):
        packet_list = packet_queue[self.id]
        while len(packet_list) > self.packets_fetched:
            pk_x, pk_y = packet_list[self.packets_fetched]
            self.packets_fetched += 1
            self.input_queue.extend([pk_x, pk_y])
            
class Network():
    
    def __init__(self, nic_code, n_nodes):
        self.nodes = []
        for i in range(n_nodes):
            self.nodes.append(NetworkNode(nic_code, i))
            packet_queue[i] = []
            
    def run_network(self):
        NAT = NATNode()
        for i, thread in enumerate(self.nodes):
            thread.start()
            
        NAT.start()
            
        for node in self.nodes:
            thread.join()
            
        NAT.join()

class NATNode(Thread):
    
    def __init__(self):
        super().__init__()
        self.address = 255
        self.network_active = 1
        self.last_packet_sent = None
        self.previous_packets_sent = 0
        self.previous_receive_attempts = 0
        self.pushed = 0
        self.answered = False
        
    def run(self):
        while True:
            self.check_network_activity()
            
    def check_network_activity(self):
        time.sleep(2)
        ps = packages_sent
        if (ps == self.previous_packets_sent):
            self.relaunch_network()
        else:
            self.previous_packets_sent = ps
            
    def relaunch_network(self):
        if 255 not in packet_queue:
            pass
        else:
            total_packages = len(packet_queue[255])
            if total_packages > self.pushed:
                to_send = packet_queue[255][-1]
                self.pushed = total_packages
                packet_queue[0].append(to_send)
                if to_send[1] == self.last_packet_sent and not self.answered:
                    print(f'Answer for part 2 is {self.last_packet_sent}')
                    self.answered = True
                self.last_packet_sent = to_send[1]
                
net = Network(code, 50)
net.run_network()
#%%
            
        
        
        
