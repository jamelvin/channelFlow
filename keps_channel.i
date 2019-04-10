Simulations:
  - name: sim1
    time_integrator: ti_1
    optimizer: opt1

linear_solvers:

  - name: solve_scalar
    type: tpetra
    method: gmres
    preconditioner: sgs
    tolerance: 1e-5
    max_iterations: 50
    kspace: 50
    output_level: 0

  - name: solve_cont
    type: tpetra
    method: gmres
    preconditioner: muelu
    tolerance: 1e-5
    max_iterations: 50
    kspace: 50
    output_level: 0
    muelu_xml_file_name: ../reg_tests/xml/milestone_aspect_ratio.xml

realms:

  - name: realm_1
    mesh: channel_Retau1000_uinf04_nu1E-5-ndtw.exo
    use_edges: no 
    check_for_missing_bcs: yes
    automatic_decomposition_type: rcb

    time_step_control:
     target_courant: 1.0
     time_step_change_factor: 1.2

    equation_systems:
      name: theEqSys
      max_iterations: 2

      solver_system_specification:
        velocity: solve_scalar
        turbulent_ke: solve_scalar
        total_dissipation_rate: solve_scalar
        #specific_dissipation_rate: solve_scalar
        pressure: solve_cont

      systems:

        #- ChienKEpsilon:
        #    name: myKE
        #    max_iterations: 1
        #    convergence_tolerance: 1e-5

        - LowMachEOM:
            name: myLowMach
            max_iterations: 1
            convergence_tolerance: 1e-5

        - ChienKEpsilon:
            name: myKE 
            max_iterations: 1
            convergence_tolerance: 1e-5
        
        #- ShearStressTransport:
        #    name: mySST
        #    max_iterations: 1
        #    convergence_tolerance: 1e-5

    initial_conditions:
      - constant: ic_1
        target_name: Unspecified-2-HEX
        value:
          pressure: 0
          velocity: [1.0,0.0,0.0]
          turbulent_ke: 0.0001
          total_dissipation_rate: 0.00001
          #specific_dissipation_rate: 3528.0

    material_properties:
      target_name: Unspecified-2-HEX
      specifications:
        - name: density
          type: constant
          value: 1.0
        - name: viscosity
          type: constant
          value: 9.99488e-4

    boundary_conditions:

    - wall_boundary_condition: bc_bot
      target_name: bottom 
      wall_user_data:
        velocity: [0,0,0]
        turbulent_ke: 0.0
        total_dissipation_rate: 0.0
        use_wall_function: no

    - wall_boundary_condition: bc_top
      target_name: top
      wall_user_data:
        velocity: [0,0,0]
        turbulent_ke: 0.0
        total_dissipation_rate: 0.0
        use_wall_function: no

    - periodic_boundary_condition: bc_inlet_outlet
      target_name: [inlet, outlet]
      periodic_user_data:
        search_tolerance: 0.001

    - periodic_boundary_condition: bc_front_back
      target_name: [front, back]
      periodic_user_data:
        search_tolerance: 0.001

    #- inflow_boundary_condition: bc_inflow
    #  target_name: inlet
    #  inflow_user_data:
    #    velocity: [0.4,0.0,0.0]
    #    turbulent_ke: 0.0005
    #    specific_dissipation_rate: 3528.883

    #- open_boundary_condition: bc_open
    #  target_name: outlet
    #  open_user_data:
    #    velocity: [0,0,0]
    #    pressure: 0.0
    #    turbulent_ke: 0.0005
    #    specific_dissipation_rate: 3528.883

    #- symmetry_boundary_condition: bc_outlet
    #  target_name: outlet
    #  symmetry_user_data:

    #- symmetry_boundary_condition: bc_inlet
    #  target_name: inlet
    #  symmetry_user_data:

    #- symmetry_boundary_condition: bc_front
    #  target_name: front
    #  symmetry_user_data:

    #- symmetry_boundary_condition: bc_back
    #  target_name: back
    #  symmetry_user_data:

    solution_options:
      name: myOptions
      turbulence_model: keps
      #turbulence_model: sst

      use_consolidated_solver_algorithm: yes

      options:
        - hybrid_factor:
            velocity: 1.0 
            turbulent_ke: 1.0
            total_dissipation_rate: 1.0
            #specific_dissipation_rate: 1.0

        - alpha_upw:
            velocity: 0.0 

        - limiter:
            pressure: no
            velocity: yes
            turbulent_ke: yes
            total_dissipation_rate: yes
            #specific_dissipation_rate: yes

        - projected_nodal_gradient:
            velocity: element
            pressure: element 
            turbulent_ke: element
            total_dissipation_rate: element
            #specific_dissipation_rate: element

        - shifted_gradient_operator:
            velocity: yes
            pressure: yes
            turbulent_ke: yes
            total_dissipation_rate: yes
            #specific_dissipation_rate: yes

        - element_source_terms:
            momentum: [momentum_time_derivative, advection_diffusion, const_body_force]
            continuity: [advection]
            turbulent_ke: [turbulent_ke_time_derivative, upw_advection_diffusion, ke]
            total_dissipation_rate: [total_dissipation_rate_time_derivative, upw_advection_diffusion, ke] 
            #specific_dissipation_rate: [specific_dissipation_rate_time_derivative, upw_advection_diffusion, sst]

        - input_variables_from_file:
            minimum_distance_to_wall: ndtw

        - turbulence_model_constants:
            utau: 1.0
            #SDRWallFactor: 0.625

        - user_constants:
            constBodyForce: [-1.00,0.0,0.0]

    output:
      output_data_base_name: results/kepsChannelNumerics.e
      output_frequency: 1000
      output_node_set: no 
      output_variables:
       - velocity
       - density
       - pressure
       - pressure_force
       - tau_wall
       - turbulent_ke
       - total_dissipation_rate
       #- specific_dissipation_rate
       - minimum_distance_to_wall
       - dplus_wall_function
       - turbulent_viscosity

    restart:
      restart_data_base_name: restart/kepsChannelNumerics.rst
      output_frequency: 5000
     
Time_Integrators:
  - StandardTimeIntegrator:
      name: ti_1
      start_time: 0
      time_step: 1.0e-2
      termination_step_count: 10000
      time_stepping_type: fixed
      time_step_count: 0
      second_order_accuracy: yes

      realms: 
        - realm_1
        
